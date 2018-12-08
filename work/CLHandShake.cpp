//---------Implement Packet CLHandShake
#include "stdafx.h"
#include "CLHandShake.h"

CLHandShake::CLHandShake()
{
};
CLHandShake::~CLHandShake()
{
}
uint32 CLHandShake::Process(Connector *pConnector) 
{ 
    return CLHandShakeDispatch::Process(this, pConnector); 
}
uint32 CLHandShake::GetMsgSize() const
{
    uint32 size=0;
    size+=sizeof(int32);
    size+=sizeof(int8);
    return size;
}
uint32 CLHandShakeFactory::GetMessageMaxSize() const
{
    uint32 size=0;
	size+=sizeof(int32);
	size+=sizeof(int8);
	return size;
}
BOOL CLHandShake::Recieve(RecieveStream &iStream) 
{ 
    iStream.Reci((char *) (&m_MagicNum), sizeof(m_MagicNum));
    iStream.Reci((char *) (&m_QuickMark), sizeof(m_QuickMark));
    return TRUE;
}
BOOL CLHandShake::Send(SendStream &oStream) const 
{ 
    iStream.Reci((char *) (&m_MagicNum), sizeof(m_MagicNum));
    iStream.Reci((char *) (&m_QuickMark), sizeof(m_QuickMark));
    return TRUE;
}
//---------Implement Packet CLHandShake End