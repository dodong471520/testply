//---------Implement Packet XCHandShake
#include "stdafx.h"
#include "CLHandShake.h"

XCHandShake::XCHandShake()
{
};
XCHandShake::~XCHandShake()
{
}
uint32 XCHandShake::Process(Connector *pConnector) 
{ 
    return XCHandShakeDispatch::Process(this, pConnector); 
}
uint32 XCHandShake::GetMsgSize() const
{
    uint32 size=0;
    size+=sizeof(int32);
    return size;
}
uint32 XCHandShakeFactory::GetMessageMaxSize() const
{
    uint32 size=0;
	size+=sizeof(int32);
	return size;
}
BOOL XCHandShake::Recieve(RecieveStream &iStream) 
{ 
    iStream.Reci((char *) (&m_RsaIndex), sizeof(m_RsaIndex));
    return TRUE;
}
BOOL XCHandShake::Send(SendStream &oStream) const 
{ 
    iStream.Reci((char *) (&m_RsaIndex), sizeof(m_RsaIndex));
    return TRUE;
}
//---------Implement Packet XCHandShake End