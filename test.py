import asyncio

from livekit import api
from livekit.protocol.sip import CreateSIPOutboundTrunkRequest, SIPOutboundTrunkInfo

async def main():
  lkapi = api.LiveKitAPI()

  trunk = SIPOutboundTrunkInfo(
    name = "My trunk",
    address = "sip.telnyx.com",
    numbers = ['+917775099809'],
    auth_username = "<username>",
    auth_password = "<password>"
  )

  request = CreateSIPOutboundTrunkRequest(
    trunk = trunk
  )

  trunk = await lkapi.sip.create_sip_outbound_trunk(request)

  print(f"Successfully created {trunk}")

  await lkapi.aclose()

asyncio.run(main())