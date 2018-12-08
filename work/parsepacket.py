from lexpacket import *
import ply.yacc as yacc
import sys
import re

REPLACE_STR = r'##{key}##|{key}##|##{key}|\b{key}\b'
def format_template(content,*keyvalue):
    content=content[1:]
    key_value_len=len(keyvalue)/2
    for index in range(key_value_len):
        key=keyvalue[index*2+0]
        value=keyvalue[index*2+1]
        re_str=REPLACE_STR.format(key=key)
        content=re.sub(re_str,value,content)
    return content

# declare 
TEMPLATE_DECLARE_PACKET_BEGIN = '''
namespace Messages 
{ 
    class MESSAGE_NAME : public IMessage 
    { 
    public: 
        MESSAGE_NAME();	
        virtual ~MESSAGE_NAME();
        virtual BOOL	Recieve(RecieveStream &iStream); 
        virtual BOOL	Send(SendStream &oStream) const; 
        virtual uint32	Process(Connector *pConnector); 
        virtual uint32 GetMsgSize() const;
        virtual MSG_ID GetMsgID() const 
        { 
            return MESSAGE_ID;
        }
'''
TEMPLATE_DECLARE_PACKET_END = '''
    }; 
    class MESSAGE_NAME##Factory : public MessageFactory 
    { 
    public: 
        IMessage *CreateMessage() 
        { 
            return new MESSAGE_NAME(); 
        } 
        MSG_ID GetMsgID() const 
        { 
            return MESSAGE_ID; 
        }
        uint32 GetMessageMaxSize() const;
    }; 
    class   MESSAGE_NAME##Dispatch 
    { 
    public: 
        static uint32	Process(MESSAGE_NAME *pMessage, Connector *pConnector); 
    }; 
}; 
using namespace Messages;
'''
# declare define
TEMPLATE_DECLARE_PACKET_DEFINE_BEGIN = '''
    private:
'''
# declare define atom
TEMPLATE_DECLARE_PACKET_VAR_DEFINE_ATOM = '''
        type	m_##x; 
'''
# declare get
TEMPLATE_DECLARE_PACKET_GET_BEGIN = '''
    public: 
'''
# declare get atom
TEMPLATE_DECLARE_PACKET_VAR_GET_ATOM = '''
        const type Get##x() const
        { 
            return m_##x; 
        } 
'''
# declare set
TEMPLATE_DECLARE_PACKET_SET_BEGIN = '''
    public:
'''
# declare set atom
TEMPLATE_DECLARE_PACKET_VAR_SET_ATOM = '''
        void Set##x(const type val)
        { 
            m_##x = val; 
        }
'''
TEMPLATE_IMPLEMENT_PACKET = '''
MESSAGE_NAME::MESSAGE_NAME()
{
};
MESSAGE_NAME::~MESSAGE_NAME()
{
}
uint32 MESSAGE_NAME::Process(Connector *pConnector) 
{ 
    __GUARD__ return MESSAGE_NAME##Dispatch::Process(this, pConnector); 
    __UNGUARD__ return FALSE; 
}
'''
#GetSize
TEMPLATE_IMPLEMENT_PACKET_GETMSGSIZE_BEGIN = '''
uint32 MESSAGE_NAME::GetMsgSize() const
{
    uint32 size=0;
'''
TEMPLATE_IMPLEMENT_PACKET_GETMSGSIZE_END = '''
    return size;
}
'''
#GetSize atom
TEMPLATE_IMPLEMENT_PACKET_GETMSGSIZE_ATOM = '''
    size+=sizeof(type);
'''
#GetMessageMaxSize
TEMPLATE_IMPLEMENT_PACKET_GETMESSAGEMAXSIZE_BEGIN = '''
uint32 MESSAGE_NAME##Factory::GetMessageMaxSize() const
{
    uint32 size=0;
'''
TEMPLATE_IMPLEMENT_PACKET_GETMESSAGEMAXSIZE_END = '''
	return size;
}
'''
#GetMessageMaxSize
TEMPLATE_IMPLEMENT_PACKET_GETMESSAGEMAXSIZE_ATOM = '''
	size+=sizeof(type);
'''


class Packet:
    def __init__(self,packet_name,packet_id):
        self.PacketName=packet_name
        self.PacketID=packet_id
        self.VarList=[]
    def ToDeclare(self):
        log = "//---------Declare Packet " + self.PacketName
        log += format_template(TEMPLATE_DECLARE_PACKET_BEGIN,"MESSAGE_NAME",self.PacketName,"MESSAGE_ID",self.PacketID)
        log += format_template(TEMPLATE_DECLARE_PACKET_DEFINE_BEGIN)
        for tmp in self.VarList:
            log += tmp.ToDeclareVar()
        log += format_template(TEMPLATE_DECLARE_PACKET_GET_BEGIN)
        for tmp in self.VarList:
            log += tmp.ToDeclareGet()
        log += format_template(TEMPLATE_DECLARE_PACKET_SET_BEGIN)
        for tmp in self.VarList:
            log += tmp.ToDeclareSet()
        log += format_template(TEMPLATE_DECLARE_PACKET_END,"MESSAGE_NAME",self.PacketName,"MESSAGE_ID",self.PacketID)
        log = "//---------Declare Packet " + self.PacketName + " End"
        return log
    def ToImplement(self):
        log = "//---------Implement Packet " + self.PacketName
        log = format_template(TEMPLATE_IMPLEMENT_PACKET)
        log += format_template(TEMPLATE_IMPLEMENT_PACKET_GETMSGSIZE_BEGIN)
        for tmp in self.VarList:
            log += tmp.ToImplement_GetSize()
        log += format_template(TEMPLATE_IMPLEMENT_PACKET_GETMSGSIZE_END)
        log += format_template(TEMPLATE_IMPLEMENT_PACKET_GETMESSAGEMAXSIZE_BEGIN)
        for tmp in self.VarList:
            log += tmp.ToImplement_GetMessageMaxSize()
        log += format_template(TEMPLATE_IMPLEMENT_PACKET_GETMESSAGEMAXSIZE_END)
        log = "//---------Implement Packet " + self.PacketName + " End"
        return log
class PacketVar:
    def __init__(self, type, value):
        self.Type = type
        self.Value = value
    def ToDeclareVar(self):
        log = format_template(TEMPLATE_DECLARE_PACKET_VAR_DEFINE_ATOM,"type",self.Type,"x",self.Value)
        return log
    def ToDeclareGet(self):
        log = format_template(TEMPLATE_DECLARE_PACKET_VAR_GET_ATOM,"x",self.Value)
        return log
    def ToDeclareSet(self):
        log = format_template(TEMPLATE_DECLARE_PACKET_VAR_SET_ATOM,"x",self.Value)
        return log
    def ToImplement_GetSize(self):
        log = format_template(TEMPLATE_IMPLEMENT_PACKET_GETMSGSIZE_ATOM,"type",self.Type)
        return log
    def ToImplement_GetMessageMaxSize(self):
        log = format_template(TEMPLATE_IMPLEMENT_PACKET_GETMESSAGEMAXSIZE_ATOM,"type",self.Type)
        return log

def p_packet(p):
    'packet : packet_begin packet_vars packet_end'
    p[0]=Packet(p[1]["packetname"],p[1]['packetid'])
    for tmp in p[2]:
        p[0].VarList.append(tmp)

def p_packet_begin(p):
    'packet_begin : DECLARE_NET_MESSAGE_BEGIN LPAREN ID COMMA ID RPAREN'
    p[0]={"packetname":p[3],"packetid":p[5]}

def p_packet_end(p):
    'packet_end : DECLARE_NET_MESSAGE_END LPAREN ID COMMA ID RPAREN'
    p[0]={"packetname":p[3],"packetid":p[5]}

def p_packet_vars_2(p):
    'packet_vars : packet_var '
    p[0] = [p[1]]

def p_packet_vars_1(p):
    'packet_vars : packet_vars packet_var'
    p[1].append(p[2])
    p[0]=p[1]

def p_packet_var(p):
    'packet_var : DECLARE_NET_MESSAGE_ATOM_VAR LPAREN ID COMMA ID RPAREN'
    p[0]=PacketVar(p[3],p[5])

# Error rule for syntax errors
def p_error(p):
    print("Syntax error " ,p)

# Build the parser
parser = yacc.yacc(tabmodule='packet',debug=True)
input_str = sys.stdin.read()
result = parser.parse(input_str)
print result.ToDeclare()
print result.ToImplement()