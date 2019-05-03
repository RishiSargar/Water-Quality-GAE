from google.appengine.ext import ndb

class Data(ndb.Model):
    timestamp = ndb.DateTimeProperty()
    controller_id = ndb.StringProperty()
    location = ndb.StringProperty()
    temperature = ndb.FloatProperty()
    ec = ndb.FloatProperty()
    ph = ndb.FloatProperty()

    @staticmethod
    def create_and_store(
        timestamp,
        controller_id,
        location,
        temperature,
        ec,
        ph,
    ):
        try:
            cd = Data(
                timestamp=timestamp,
                controller_id=controller_id,
                location=location,
                temperature=temperature,
                ec=ec,
                ph=ph,
            )
            cd.put()

            return True
        except:
            return False