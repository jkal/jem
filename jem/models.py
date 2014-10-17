import peewee as pw

db_proxy = pw.Proxy()

class BaseModel(pw.Model):
    class Meta:
        database = db_proxy

class Asset(BaseModel):
    name = pw.CharField(unique=True)

    def __repr__(self):
        return '%s:%s' % (self.id, self.name) 

class Tag(BaseModel):
    name = pw.CharField(unique=True)

    def __repr__(self):
        return '%s:%s' % (self.id, self.name) 

class AssetTag(BaseModel):
    asset = pw.ForeignKeyField(Asset)
    tag = pw.ForeignKeyField(Tag)
