from lexc import *
add_reserved('DECLARE_NET_MESSAGE_BEGIN','DECLARE_NET_MESSAGE_BEGIN')
add_reserved('DECLARE_NET_MESSAGE_ATOM_VAR','DECLARE_NET_MESSAGE_ATOM_VAR')
add_reserved('DECLARE_NET_MESSAGE_END','DECLARE_NET_MESSAGE_END')
lex.lex()

# declare packet
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
# implement packet
TEMPLATE_IMPLEMENT_PACKET_BEGIN = '''
MESSAGE_NAME::MESSAGE_NAME()
{
};
MESSAGE_NAME::~MESSAGE_NAME()
{
}
uint32 MESSAGE_NAME::Process(Connector *pConnector) 
{ 
    return MESSAGE_NAME##Dispatch::Process(this, pConnector); 
}
'''
# implement GetSize
TEMPLATE_IMPLEMENT_PACKET_GETMSGSIZE_BEGIN = '''
uint32 MESSAGE_NAME::GetMsgSize() const
{
    uint32 size=0;
'''
TEMPLATE_IMPLEMENT_PACKET_GETMSGSIZE_END = '''
    return size;
}
'''
# implement GetSize atom
TEMPLATE_IMPLEMENT_PACKET_GETMSGSIZE_ATOM = '''
    size+=sizeof(type);
'''
# implement GetMessageMaxSize
TEMPLATE_IMPLEMENT_PACKET_GETMESSAGEMAXSIZE_BEGIN = '''
uint32 MESSAGE_NAME##Factory::GetMessageMaxSize() const
{
    uint32 size=0;
'''
TEMPLATE_IMPLEMENT_PACKET_GETMESSAGEMAXSIZE_END = '''
	return size;
}
'''
# implement GetMessageMaxSize
TEMPLATE_IMPLEMENT_PACKET_GETMESSAGEMAXSIZE_ATOM = '''
	size+=sizeof(type);
'''
# implement Recieve
TEMPLATE_IMPLEMENT_PACKET_RECIEVE_BEGIN = '''
BOOL MESSAGE_NAME::Recieve(RecieveStream &iStream) 
{ 
'''
TEMPLATE_IMPLEMENT_PACKET_RECIEVE_END = '''
    return TRUE;
}
'''
# implement GetSize atom
TEMPLATE_IMPLEMENT_PACKET_RECIEVE_ATOM = '''
    iStream.Reci((char *) (&m_##x), sizeof(m_##x));
'''
# implement Send
TEMPLATE_IMPLEMENT_PACKET_SEND_BEGIN = '''
BOOL MESSAGE_NAME::Send(SendStream &oStream) const 
{ 
'''
TEMPLATE_IMPLEMENT_PACKET_SEND_END = '''
    return TRUE;
}
'''
# implement Send atom
TEMPLATE_IMPLEMENT_PACKET_SEND_ATOM = '''
    iStream.Reci((char *) (&m_##x), sizeof(m_##x));
'''

class Packet:
    def __init__(self,packet_name,packet_id):
        self.PacketName=packet_name
        self.PacketID=packet_id
        self.VarList=[]
        self.ScopeList=[]
    def ToDefine(self,index):
        return "\t\t"+self.PacketName+"\t\t\t=\t"+str(index)+",\n"
    def ToDeclare(self):
        header_name = re.sub(r'[A-Z]',lambda x:"_"+x.group(0),self.PacketName)
        log = "//---------Declare Packet " + self.PacketName  + "\n"
        log += "#ifndef "+header_name+"_" + "\n"
        log += "#define "+header_name+"_" + "\n" + "\n"
        log += format_template(TEMPLATE_DECLARE_PACKET_BEGIN,"MESSAGE_NAME",self.PacketName,"MESSAGE_ID",self.PacketID)
        # declare var
        log += format_template(TEMPLATE_DECLARE_PACKET_DEFINE_BEGIN)
        for tmp in self.VarList:
            log += tmp.ToDeclareVar()
        # declare get
        log += format_template(TEMPLATE_DECLARE_PACKET_GET_BEGIN)
        for tmp in self.VarList:
            log += tmp.ToDeclareGet()
        # declare set
        log += format_template(TEMPLATE_DECLARE_PACKET_SET_BEGIN)
        for tmp in self.VarList:
            log += tmp.ToDeclareSet()
        log += format_template(TEMPLATE_DECLARE_PACKET_END,"MESSAGE_NAME",self.PacketName,"MESSAGE_ID",self.PacketID) + "\n"
        log += "#endif //"+header_name+"_" + "\n"
        return log
    def ToImplement(self):
        log = "//---------Implement Packet " + self.PacketName + "\n"
        log += '#include "stdafx.h"' + "\n"
        log += '#include "CLHandShake.h"' + "\n" + "\n"
        log += format_template(TEMPLATE_IMPLEMENT_PACKET_BEGIN,"MESSAGE_NAME",self.PacketName)
        # implement GetMsgSize
        log += format_template(TEMPLATE_IMPLEMENT_PACKET_GETMSGSIZE_BEGIN,"MESSAGE_NAME",self.PacketName)
        for tmp in self.VarList:
            log += tmp.ToImplement_GetSize()
        log += format_template(TEMPLATE_IMPLEMENT_PACKET_GETMSGSIZE_END)
        # implement GetMessageMaxSize
        log += format_template(TEMPLATE_IMPLEMENT_PACKET_GETMESSAGEMAXSIZE_BEGIN,"MESSAGE_NAME",self.PacketName)
        for tmp in self.VarList:
            log += tmp.ToImplement_GetMessageMaxSize()
        log += format_template(TEMPLATE_IMPLEMENT_PACKET_GETMESSAGEMAXSIZE_END)
        # implement Recieve
        log += format_template(TEMPLATE_IMPLEMENT_PACKET_RECIEVE_BEGIN,"MESSAGE_NAME",self.PacketName)
        for tmp in self.VarList:
            log += tmp.ToImplement_Recieve()
        log += format_template(TEMPLATE_IMPLEMENT_PACKET_RECIEVE_END)
        # implement Send
        log += format_template(TEMPLATE_IMPLEMENT_PACKET_SEND_BEGIN,"MESSAGE_NAME",self.PacketName)
        for tmp in self.VarList:
            log += tmp.ToImplement_Send()
        log += format_template(TEMPLATE_IMPLEMENT_PACKET_SEND_END)
        log += "//---------Implement Packet " + self.PacketName + " End"
        return log
class PacketVar:
    def __init__(self, type, value):
        self.Type = type
        self.Value = value
    def ToDeclareVar(self):
        return format_template(TEMPLATE_DECLARE_PACKET_VAR_DEFINE_ATOM,"type",self.Type,"x",self.Value)
    def ToDeclareGet(self):
        return format_template(TEMPLATE_DECLARE_PACKET_VAR_GET_ATOM,"x",self.Value)
    def ToDeclareSet(self):
        return format_template(TEMPLATE_DECLARE_PACKET_VAR_SET_ATOM,"x",self.Value)
    def ToImplement_GetSize(self):
        return format_template(TEMPLATE_IMPLEMENT_PACKET_GETMSGSIZE_ATOM,"type",self.Type)
    def ToImplement_GetMessageMaxSize(self):
        return format_template(TEMPLATE_IMPLEMENT_PACKET_GETMESSAGEMAXSIZE_ATOM,"type",self.Type)
    def ToImplement_Recieve(self):
        return format_template(TEMPLATE_IMPLEMENT_PACKET_RECIEVE_ATOM,"x",self.Value)
    def ToImplement_Send(self):
        return format_template(TEMPLATE_IMPLEMENT_PACKET_SEND_ATOM,"x",self.Value)

def p_packets_1(p):
    'packets : packet'
    p[0] = [p[1]]
def p_packets_2(p):
    'packets : packets packet'
    p[1].append(p[2])
    p[0]=p[1]
def p_packet(p):
    'packet : packet_begin packet_vars packet_end'
    p[0]=Packet(p[1]["packetname"],p[1]['packetid'])
    for tmp in p[2]:
        p[0].VarList.append(tmp)
    p[0].ScopeList=p[3]
def p_packet_begin(p):
    'packet_begin : DECLARE_NET_MESSAGE_BEGIN LPAREN ID COMMA ID RPAREN'
    p[0]={"packetname":p[3],"packetid":p[5]}
def p_packet_end(p):
    'packet_end : DECLARE_NET_MESSAGE_END LPAREN packet_scopes RPAREN'
    p[0]=p[3]
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
def p_packet_scopes_1(p):
    'packet_scopes : packet_scopes COMMA ID'
    p[1].append(p[3])
    p[0]=p[1]
def p_packet_scopes_2(p):
    'packet_scopes : ID'
    p[0]=[p[1]]

# Error rule for syntax errors
def p_error(p):
    tok = parser.token()
    parser.errok()
    return tok
# Build the parser
parser = yacc.yacc(tabmodule='tmp_parse_packet',debug=True)
input_str = sys.stdin.read()
result = parser.parse(input_str)

# output cpp h file
for packet in result:
    f = open("Build/"+packet.PacketName+".h",'w')
    f.write(packet.ToDeclare())
    f.close()
    f = open("Build/"+packet.PacketName+".cpp",'w')
    f.write(packet.ToImplement())
    f.close()
# output messagedefine file
message_define_begin='''
#ifndef __MESSAGE_DEFINE_H__
#define __MESSAGE_DEFINE_H__

namespace	Messages
{
    enum MSG_DEFINE
    {
'''
message_define_end='''
    };
};

#endif
'''
message_packet_define='''
	MESSAGE_NONE					= 0,
'''
message_define_str=message_define_begin
message_define_index=0
for packet in result:
    message_define_str+=packet.ToDefine(message_define_index)
    message_define_index=message_define_index+1
message_define_str+=message_define_end
f = open("Build/MessageDefine.h",'w')
f.write(message_define_str)
f.close()
#output register file
SCOPE_DEFINE_LIST = [
    '_CLIENT',
    '_LOGIN'
]
client_list=[]
login_list=[]
register_list={}
for packet in result:
    key_str=""
    temp_list=[]
    for index,scope in enumerate(SCOPE_DEFINE_LIST):
        if scope in packet.ScopeList:
            temp_list.append(index)
    temp_list=tuple(temp_list)
    if not register_list.has_key(temp_list):
        register_list[temp_list]=[]
    register_list[temp_list].append(packet)
            
message_register_begin='''
#include MessageFactoryManager.h"
'''
message_register_init_begin='''
BOOL MessageFactoryManager::Init()
{
'''
message_register_init_end='''
}

'''
message_register_str=message_register_begin
for key,value in register_list.items():
    message_register_str+='\n#if defined('+SCOPE_DEFINE_LIST[key[0]]+')'
    for index in range(1,len(key)):
        message_register_str+='|| defined('+SCOPE_DEFINE_LIST[key[index]]+')'
    message_register_str+="\n"
    for packet in value:
        message_register_str+='#include "'+packet.PacketName+'.h"'+"\n"
    message_register_str+="#endif"+"\n"
message_register_str+=message_register_init_begin
for key,value in register_list.items():
    message_register_str+='\n#if defined('+SCOPE_DEFINE_LIST[key[0]]+')'
    for index in range(1,len(key)):
        message_register_str+='|| defined('+SCOPE_DEFINE_LIST[key[index]]+')'
    message_register_str+="\n"
    for packet in value:
        message_register_str+="   ADD_MSG_FACTORY("+packet.PacketName+")"+"\n"
    message_register_str+="#endif"+"\n"
message_register_str+=message_register_init_end

f = open("Build/MessageRegister.cpp",'w')
f.write(message_register_str)
f.close()
