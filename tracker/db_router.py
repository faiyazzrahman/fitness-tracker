class ProfileRouter:
    BODY_TYPE_DBS = {
        'thin': 'thin',
        'medium': 'medium',
        'fat': 'fat',
    }

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'tracker':
            if 'instance' in hints and hasattr(hints['instance'], 'body_type'):
                return self.BODY_TYPE_DBS.get(hints['instance'].body_type, 'default')
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'tracker':
            instance = hints.get('instance')
            if instance and hasattr(instance, 'body_type'):
                return self.BODY_TYPE_DBS.get(instance.body_type, 'default')
            return 'default'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        db_list = list(self.BODY_TYPE_DBS.values()) + ['default']
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label != 'tracker':
            return db == 'default'
        return db in self.BODY_TYPE_DBS.values() or db == 'default'