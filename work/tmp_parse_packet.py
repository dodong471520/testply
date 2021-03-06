
# tmp_parse_packet.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = '41B56CC4EC4F06604B3BFCF0AF551430'
    
_lr_action_items = {'DECLARE_NET_MESSAGE_BEGIN':([0,2,3,6,12,23,],[1,1,-1,-2,-3,-5,]),'RPAREN':([18,19,20,25,26,],[22,23,-10,27,-9,]),'DECLARE_NET_MESSAGE_ATOM_VAR':([4,7,8,11,22,27,],[9,-6,9,-7,-4,-8,]),'LPAREN':([1,9,13,],[5,14,16,]),'COMMA':([10,17,19,20,26,],[15,21,24,-10,-9,]),'DECLARE_NET_MESSAGE_END':([7,8,11,27,],[-6,13,-7,-8,]),'ID':([5,14,15,16,21,24,],[10,17,18,20,25,26,]),'$end':([2,3,6,12,23,],[0,-1,-2,-3,-5,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'packet_var':([4,8,],[7,11,]),'packet_scopes':([16,],[19,]),'packet_vars':([4,],[8,]),'packets':([0,],[2,]),'packet':([0,2,],[3,6,]),'packet_end':([8,],[12,]),'packet_begin':([0,2,],[4,4,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> packets","S'",1,None,None,None),
  ('packets -> packet','packets',1,'p_packets_1','parsepacket.py',222),
  ('packets -> packets packet','packets',2,'p_packets_2','parsepacket.py',225),
  ('packet -> packet_begin packet_vars packet_end','packet',3,'p_packet','parsepacket.py',229),
  ('packet_begin -> DECLARE_NET_MESSAGE_BEGIN LPAREN ID COMMA ID RPAREN','packet_begin',6,'p_packet_begin','parsepacket.py',235),
  ('packet_end -> DECLARE_NET_MESSAGE_END LPAREN packet_scopes RPAREN','packet_end',4,'p_packet_end','parsepacket.py',238),
  ('packet_vars -> packet_var','packet_vars',1,'p_packet_vars_2','parsepacket.py',241),
  ('packet_vars -> packet_vars packet_var','packet_vars',2,'p_packet_vars_1','parsepacket.py',244),
  ('packet_var -> DECLARE_NET_MESSAGE_ATOM_VAR LPAREN ID COMMA ID RPAREN','packet_var',6,'p_packet_var','parsepacket.py',248),
  ('packet_scopes -> packet_scopes COMMA ID','packet_scopes',3,'p_packet_scopes_1','parsepacket.py',251),
  ('packet_scopes -> ID','packet_scopes',1,'p_packet_scopes_2','parsepacket.py',255),
]
