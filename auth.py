from mcp.server.auth.provider import AccessToken, TokenVerifier
import os
import logging
import sys
from typing import Any, Dict, Optional
import httpx
import time
import jwt
import contextvars
import json

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)


# API configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:3011')
API_KEY = os.getenv('API_KEY', '')
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '75'))
PORT = int(os.getenv("PORT", 9000))

# MCP OAuth configuration with trailing slash fix
AUTHORIZATION_SERVER_URL = os.getenv(
    'AUTHORIZATION_SERVER_URL', 'https://auth-mcp.pilleo.ca')
RESOURCE_SERVER_URL = os.getenv(
    'RESOURCE_SERVER_URL', f'https://ai-dev-shipra.pilleo.ca')
CANONICAL_URI = os.getenv('CANONICAL_URI', f'https://ai-dev-shipra.pilleo.ca/')
STOCK_BACKEND_SERVER_URL = "https://api-shipra-v3.pilleo.ca"

request_data = contextvars.ContextVar('request_data', default={})


class MCPOAuthTokenVerifier(TokenVerifier):
    """
    MCP OAuth Token Verifier with Auto-Discovery Support

    When token verification fails, FastMCP will return 401 with WWW-Authenticate header
    pointing to the authorization server's protected resource metadata endpoint.
    This triggers the OAuth 2.1 discovery flow in MCP clients.
    """

    def __init__(self):
        self.jwks_cache = {}
        self.jwks_cache_expiry = 0
        self.authorization_server_url = AUTHORIZATION_SERVER_URL.rstrip('/')
        self.canonical_uri = CANONICAL_URI

    async def get_authorization_server_metadata(self) -> Dict[str, Any]:
        """Get authorization server metadata per RFC8414"""
        try:
            async with httpx.AsyncClient() as client:
                well_known_url = f"{self.authorization_server_url}/.well-known/oauth-authorization-server"
                logger.info(
                    f"Fetching authorization server metadata from: {well_known_url}")

                response = await client.get(well_known_url, timeout=30)
                response.raise_for_status()
                return response.json()

        except Exception as e:
            logger.error(
                f"Failed to fetch authorization server metadata: {str(e)}")
            raise Exception(
                f"Could not fetch metadata from {self.authorization_server_url}: {str(e)}")

    async def get_jwks(self) -> Dict[str, Any]:
        """Fetch JWKS from the authorization server"""
        current_time = time.time()

        # Check cache (cache for 1 hour)
        if self.jwks_cache and current_time < self.jwks_cache_expiry:
            return self.jwks_cache

        try:
            # Get authorization server metadata first
            metadata = await self.get_authorization_server_metadata()
            jwks_uri = metadata.get('jwks_uri')

            if not jwks_uri:
                raise Exception(
                    "No jwks_uri found in authorization server metadata")

            async with httpx.AsyncClient() as client:
                logger.info(f"Fetching JWKS from: {jwks_uri}")
                jwks_response = await client.get(jwks_uri, timeout=30)
                jwks_response.raise_for_status()

                self.jwks_cache = jwks_response.json()
                self.jwks_cache_expiry = current_time + 3600  # Cache for 1 hour

                return self.jwks_cache

        except Exception as e:
            logger.error(f"Failed to fetch JWKS: {str(e)}")
            raise Exception(f"Could not fetch JWKS: {str(e)}")

    async def verify_token(self, token: str) -> Optional[AccessToken]:
        """
        Verify token and enable auto-discovery on failure

        If this returns None, FastMCP automatically:
        1. Returns 401 Unauthorized 
        2. Includes WWW-Authenticate header with metadata URL
        3. Client discovers auth server from metadata
        4. Client redirects user to auth server login page
        """
        print("in verify_token")
        try:

            # First decode without verification to see contents for debugging
            try:
                unverified = jwt.decode(
                    token, options={"verify_signature": False})

                # Check audience match before expensive verification
                token_audience = unverified.get('aud')
                if token_audience != self.canonical_uri:
                    logger.error(f"❌ AUDIENCE MISMATCH!")
                    logger.error(f"   Token audience:    '{token_audience}'")
                    logger.error(
                        f"   Expected audience: '{self.canonical_uri}'")
                    logger.error(
                        f"   🔧 Fix: Set CANONICAL_URI={token_audience}")
                    return None
                else:
                    logger.info(f"✅ Audience matches: {token_audience}")

            except Exception as e:
                logger.error(f"❌ Failed to decode token for debugging: {e}")
                return None

            # Get the header to find the key ID
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get('kid')

            if not kid:
                logger.error("❌ Token missing 'kid' in header")
                return None

            jwks = await self.get_jwks()

            # Find the key
            key_data = None
            available_kids = []
            for key in jwks.get('keys', []):
                key_kid = key.get('kid')
                available_kids.append(key_kid)
                if key_kid == kid:
                    key_data = key
                    break

            if not key_data:
                logger.error(f"❌ Key with kid '{kid}' not found in JWKS!")
                logger.error(f"   Available keys: {available_kids}")
                return None

            # Convert JWK to PEM format for verification
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(
                json.dumps(key_data))

            # Verify and decode the token
            decoded = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                issuer=self.authorization_server_url,
                audience=self.canonical_uri  # This must match exactly!
            )
            print("decoded : ", decoded)
            request_data.set(decoded)

            # MCP Requirement: Validate audience (already done above, but double-check)
            audience = decoded.get("aud")
            if audience != self.canonical_uri:
                logger.error(f"❌ Final audience check failed!")
                logger.error(f"   Token audience: {audience}")
                logger.error(f"   Expected: {self.canonical_uri}")
                return None

            # Parse scopes - handle both string and list formats
            scope_value = decoded.get("scope", "")
            if isinstance(scope_value, str):
                scopes = scope_value.split() if scope_value else []
            elif isinstance(scope_value, list):
                scopes = scope_value
            else:
                scopes = []

            # Create AccessToken with correct field names
            return AccessToken(
                token=token,  # The actual token string
                sub=decoded.get("sub"),
                # Extract client_id from token
                client_id=decoded.get("client_id"),
                scopes=scopes,  # Use 'scopes' not 'scope'
                exp=decoded.get("exp")
            )

        except jwt.ExpiredSignatureError:
            logger.error("❌ Token expired")
        except jwt.InvalidIssuerError:
            logger.error(f"❌ Invalid token issuer")
            logger.error(
                f"   Expected issuer: {self.authorization_server_url}")
        except jwt.InvalidAudienceError:
            logger.error(f"❌ Invalid token audience")
            logger.error(f"   Expected audience: {self.canonical_uri}")
            logger.error(
                f"   🔧 Fix: Update CANONICAL_URI to match token audience exactly")
        except jwt.InvalidTokenError as e:
            logger.error(f"❌ Invalid token: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Token verification error: {str(e)}")
            logger.error(f"   Error type: {type(e).__name__}")

        return None
