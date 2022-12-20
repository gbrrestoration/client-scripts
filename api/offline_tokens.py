import typer
import os
from mdsisclienttools.auth.TokenManager import DeviceFlowManager, AuthFlow
from config import *

# try to avoid leaking creds to CLI output - don't show local vars on exception
app = typer.Typer(pretty_exceptions_show_locals=False)


def write_to_file(token: str, file: typer.FileTextWrite) -> None:
    with file as f:
        f.write(token)


@app.command()
def test_offline_token(
    stage: Stage = typer.Argument(
        ...,
        help="The stage to target - auth server is determined by stage."
    )
) -> None:
    """ 
    Tests that the provided offline token allows login. Must have an environment
    variable called RRAP_OFFLINE_TOKEN which contains the valid offline access token.
    """

    # special keycloak client configured for offline access
    client_id = "automated-access"

    # get the token
    token = os.environ.get("RRAP_OFFLINE_TOKEN")

    if token is None:
        raise ValueError(
            "There was no RRAP_OFFLINE_TOKEN environment variable.")

    # remove any unwanted whitespace
    token.strip()

    # get the respective keycloak endpoint for the stage
    keycloak_endpoint = AUTH_SERVER_STAGE_MAP[stage]

    print("Logging into automated-access client using offline authorisation flow.")

    # initiate a device auth flow
    manager = DeviceFlowManager(
        stage=stage,
        keycloak_endpoint=keycloak_endpoint,
        client_id=client_id,
        auth_flow=AuthFlow.OFFLINE,
        offline_token=token,
        force_token_refresh=True
    )

    print("Success!")


@app.command()
def generate_offline_token(
    stage: Stage = typer.Argument(
        ...,
        help="The stage to target - auth server is determined by stage."
    ),
    output_file: typer.FileTextWrite = typer.Argument(
        ...,
        help="The name of the file to output plain text token to - ensure it is stored securely."
    )
) -> None:
    """ 
    Produces an offline token by completing an OAuth device grant against the
    configured keycloak client and requesting the offline access scope.
    """

    # grant scope
    scopes = ["offline_access"]

    # special keycloak client configured for offline access
    client_id = "automated-access"

    # get the respective keycloak endpoint for the stage
    keycloak_endpoint = AUTH_SERVER_STAGE_MAP[stage]

    print("Logging into automated-access client using device authorisation flow.")

    # initiate a device auth flow
    manager = DeviceFlowManager(
        stage=stage,
        keycloak_endpoint=keycloak_endpoint,
        client_id=client_id,
        auth_flow=AuthFlow.DEVICE,
        scopes=scopes,
        force_token_refresh=True
    )

    print("Login complete - offline token generated.")

    # if successful, pull out the offline access token (refresh token)
    offline_token = manager.tokens.refresh_token
    assert offline_token

    # write to output file
    write_to_file(
        token=offline_token,
        file=output_file
    )


if __name__ == "__main__":
    app()
