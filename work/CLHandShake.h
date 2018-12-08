//---------Declare Packet CLHandShake
#ifndef _C_L_Hand_Shake_
#define _C_L_Hand_Shake_

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

#endif //_C_L_Hand_Shake_
