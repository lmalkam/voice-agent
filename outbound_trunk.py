import asyncio

from livekit import api
from livekit.protocol.sip import CreateSIPOutboundTrunkRequest, SIPOutboundTrunkInfo

async def main():
  lkapi = api.LiveKitAPI()

  trunk = SIPOutboundTrunkInfo(
    name = "LiveKit Trunk",
    address = "livekit-trunk-82460739.pstn.twilio.com",
    numbers = ['+18787686085'],
    auth_username = "linesh",
    auth_password = "Linux2k3!!!7775099809"
  )

  request = CreateSIPOutboundTrunkRequest(
    trunk = trunk
  )

  trunk = await lkapi.sip.create_sip_outbound_trunk(request)

  print(f"Successfully created {trunk}")

  await lkapi.aclose()

asyncio.run(main())