
class Registry(object):
    '''
    Act as global dictinary for config to call the model 

    regist usage 
        ```
        @Registry_Obj.regist
        class .... 
        ```
    call usage 
        ```
        Registry_Obj
        ```
    
    '''
    def __init__(self, name):
        '''
        Args:
          - instanlized : if True, the registed class will init. as instance
        '''
        self._name = name
        self._module_dict = dict()

    @property
    def name(self):
        return self._name

    @property
    def module_dict(self):
        return self._module_dict

    def __call__(self, name):
        try:
            return self._module_dict[name]
        except:
            raise KeyError('{} is not existed in {}'.format(
                name, self.name))
            
    def _register_module(self, cls_obj):
        """ Register a module.
        """
        cls_name = cls_obj.__name__
        if cls_name in self._module_dict:
            raise KeyError('{} is already registered in {}'.format(
                cls_name, self.name))

        self._module_dict[cls_name] = cls_obj

    def on(self, cls):
        self._register_module(cls)
        return cls

RegisterModel  = Registry('Model')