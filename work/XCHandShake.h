//---------Declare Packet XCHandShake
#ifndef _X_C_Hand_Shake_
#define _X_C_Hand_Shake_

namespace Messages
{ 
    class XCHandShake : public IMessage 
    { 
    public: 
        XCHandShake();	
        virtual ~XCHandShake();
        virtual BOOL	Recieve(RecieveStream &iStream); 
        virtual BOOL	Send(SendStream &oStream) const; 
        virtual uint32	Process(Connector *pConnector); 
        virtual uint32 GetMsgSize() const;
        virtual MSG_ID GetMsgID() const 
        { 
            return MESSAGE_LC_RETCONNECT;
        }
    private:
        int32	m_RsaIndex; 
    public: 
        const type GetRsaIndex() const
        { 
            return m_RsaIndex; 
        } 
    public:
        void SetRsaIndex(const type val)
        { 
            m_RsaIndex = val; 
        }
    }; 
    class XCHandShakeFactory : public MessageFactory 
    { 
    public: 
        IMessage *CreateMessage() 
        { 
            return new XCHandShake(); 
        } 
        MSG_ID GetMsgID() const 
        { 
            return MESSAGE_LC_RETCONNECT; 
        }
        uint32 GetMessageMaxSize() const;
    }; 
    class   XCHandShakeDispatch 
    { 
    public: 
        static uint32	Process(XCHandShake *pMessage, Connector *pConnector); 
    }; 
}; 
using namespace Messages;

#endif //_X_C_Hand_Shake_
