""" Virtual Class Example """

import os
import pymel.all as pm
import xml.etree.cElementTree as cetree

class MyVirtualNode(pm.nt.Network):
    """ this is an example of how to create your own subdivisions of existing nodes. """
    @classmethod
    def list(cls,*args,**kwargs):
        """ Returns all instances the node in the scene """

        kwargs['type'] = cls.__melnode__
        return [ node for node in pm.ls(*args,**kwargs) if isinstance(node,cls)]

    @classmethod
    def _isVirtual( cls, obj, name ):
        """PyMEL code should not be used inside the callback, only API and maya.cmds. """
        fn = pm.api.MFnDependencyNode(obj)
        try:
            if fn.hasAttribute('myString'):
                plug = fn.findPlug('myString')
                if plug.asString() == 'virtualNode':
                    return True
                return False
        except:
            pass
        return False

    @classmethod
    def _preCreateVirtual(cls, **kwargs ):
        """This is called before creation. python allowed."""
        return kwargs

    @classmethod
    def _postCreateVirtual(cls, newNode ):
        """ This is called before creation, pymel/cmds allowed."""
        newNode.addAttr('myName', dt='string')        
        
        newNode.addAttr('myString', dt='string')
        newNode.myString.set('virtualNode')

        newNode.addAttr('myFloat', at='float')
        newNode.myFloat.set(.125)

        newNode.addAttr('myConnection', at='message')

    # Getters and setters are not required, we have these here for unittesting
    def get_my_name(self):
        return self.myName.get()
    
    def set_my_name(self,value):
        self.myName.set(value)
        
    def get_my_string(self):
        return self.myString.get()
        
    def set_my_string(self, value):
        self.myString.set(value)

    def get_my_float(self):
        return self.myFloat.get()

    def set_my_float(self, value):
        self.myFloat.set(value)

    def get_my_connection(self, index=0):
        return self.myConnection.listConnections()[index]
    
    def set_my_connection(self, node):
        self.myConnection.connect(node.blackBox)
    
    def toXML(self):
        xml = cetree.Element('MyVirtualNode')
        xml.set('Name', self.get_my_name())
            
        return xml
    
class MyVirtualSubNode(MyVirtualNode):
    
    SUBNODE_TYPE = 'subNodeTypeA'
    
    @classmethod
    def list(cls,*args,**kwargs):
        """ Returns all instances of all characters in the scene """

        kwargs['type'] = cls.__melnode__
        return [ node for node in pm.ls(*args,**kwargs) if isinstance(node,cls)]

    @classmethod
    def _isVirtual( cls, obj, name ):
        """PyMEL code should not be used inside the callback, only API and maya.cmds. """
        fn = pm.api.MFnDependencyNode(obj)
        try:
            if fn.hasAttribute('myString'):
                plug = fn.findPlug('myString')
                if plug.asString() == 'virtualNode':
                    if fn.hasAttribute('mySubNodeType'):
                        plug = fn.findPlug('mySubNodeType')
                        if plug.asString() == cls.SUBNODE_TYPE:
                            return True
                    return False
        except:
            pass
        return False    
    
    @classmethod
    def _postCreateVirtual(cls, newNode ):
        """ This is called before creation, pymel/cmds allowed."""
        MyVirtualNode._postCreateVirtual(newNode)
        newNode.addAttr('mySubNodeType', dt='string')
        newNode.mySubNodeType.set('subNodeTypeA')
    
pm.factories.registerVirtualClass( MyVirtualNode )
pm.factories.registerVirtualClass( MyVirtualSubNode, nameRequired=False )