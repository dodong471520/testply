"dsafsafsa"
//---------Declare Packet CLHandShake
namespace Messages 
{ 
    class CLHandShake : public IMessage 
    { 
    public: 
        CLHandShake();	
        virtual ~CLHandShake();
        virtual BOOL	Recieve(RecieveStream &iStream); 
        virtual BOOL	Send(SendStream &oStream) const; 
        virtual uint32	Process(Connector *pConnector); 
        virtual uint32 GetMsgSize() const;
        virtual MSG_ID GetMsgID() const 
        { 
            return MESSAGE_CL_CONNECT;
        }
    private:
        int32	m_MagicNum; 
        int8	m_QuickMark; 
    public: 
        const type GetMagicNum() const
        { 
            return m_MagicNum; 
        } 
        const type GetQuickMark() const
        { 
            return m_QuickMark; 
        } 
    public:
        void SetMagicNum(const type val)
        { 
            m_MagicNum = val; 
        }
        void SetQuickMark(const type val)
        { 
            m_QuickMark = val; 
        }
    }; 
    class CLHandShakeFactory : public MessageFactory 
    { 
    public: 
        IMessage *CreateMessage() 
        { 
            return new CLHandShake(); 
        } 
        MSG_ID GetMsgID() const 
        { 
            return MESSAGE_CL_CONNECT; 
        }
        uint32 GetMessageMaxSize() const;
    }; 
    class   CLHandShakeDispatch 
    { 
    public: 
        static uint32	Process(CLHandShake *pMessage, Connector *pConnector); 
    }; 
}; 
using namespace Messages;
//---------Declare Packet CLHandShake End

//---------Implement Packet CLHandShake
CLHandShake::CLHandShake()
{
};
CLHandShake::~CLHandShake()
{
}
uint32 CLHandShake::Process(Connector *pConnector) 
{ 
    __GUARD__ return CLHandShakeDispatch::Process(this, pConnector); 
    __UNGUARD__ return FALSE; 
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

