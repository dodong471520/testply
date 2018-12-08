#ifndef _KHANCL_CONNECT_H_
#define _KHANCL_CONNECT_H_

#include "TypeDefine.h"
#include "Message.h"
#include "MessageFactory.h"


DECLARE_NET_MESSAGE_BEGIN(CLHandShake, MESSAGE_CL_CONNECT)
DECLARE_NET_MESSAGE_ATOM_VAR(int32,MagicNum)
DECLARE_NET_MESSAGE_ATOM_VAR(int8,QuickMark)		// 定义快速注册的标志
DECLARE_NET_MESSAGE_END(CLHandShake, MESSAGE_CL_CONNECT)

#endif