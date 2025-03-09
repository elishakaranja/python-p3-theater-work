from sqlalchemy import ForeignKey, Column, Integer, String, MetaData,Boolean,create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)
#creating engine 
my_engine = create_engine("sqlite:///auditions.db")
Base.metadata.create_all(my_engine)



Session = sessionmaker(bind=my_engine)
session = Session()

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer(),primary_key = True)
    character_name = Column(String(),nullable = False)

    #relationship (one role has many auditions)
    auditions = relationship('Audition',back_populates = 'role')

    def actors(self):
        """Returns a list of actor names for this role"""
        return [audition.actor for audition in self.auditions]

    def locations(self):
        """Returns a list of locations from the auditions"""
        return [audition.location for audition in self.auditions]

    def lead(self):
        """Returns the first hired actor or 'no actor has been hired for this role'"""
        hired_actors = [audition for audition in self.auditions if audition.hired]
        return hired_actors[0] if hired_actors else "No actor has been hired for this role."

    def understudy(self):
        """Returns the second hired actor or 'no actor has been hired for understudy'"""
        hired_actors = [audition for audition in self.auditions if audition.hired]
        return hired_actors[1] if len(hired_actors) > 1 else "No actor has been hired for understudy for this role."
    


class Audition(Base):
    __tablename__ = 'auditions'
    id = Column(Integer(),primary_key = True)
    actor = Column(String(),nullable = False)
    location = Column(String(),nullable = False)
    phone = Column(Integer(),nullable = False)
    hired = Column(Boolean(),default = False) 
    role_id = Column(Integer(),ForeignKey('roles.id'))#every audition belongs to a role 

    # Relationship (each Audition belongs to one Role)
    role = relationship('Role',back_populates = 'auditions')

    def call_back(self):
        """Marks the audition as hired"""
        self.hired = True
    # #Audition.role returns an instance of role associated with this audition.
    # def role(self):
    #     the_role = Audition.role
    #     return the_role
    
# role1 = Role(character_name = "Mr.Bean")

# session.add(role1)
# session.commit()

#role = session.query(Role).filter_by(character_name="Mr.Bean").first()



#Create role 
hamlet = Role(character_name = "Hamlet")
lady_bug = Role(character_name = "lady bug")


# Create auditions for that role
#audition1 = Audition(actor="Elisha ", location="Nairobi", phone="123-456-7890", role=role)
audition1 = Audition(actor='Didi', location = "Nairobi",phone = "1234567",role = hamlet) 
audition2 = Audition(actor = 'Amani Kimberly',location = "Nairobi",phone = "072864444", role = lady_bug)

# Add to the session and commit
session.add(audition2)
session.commit()#auditions added 

# #query
# hamlet_query = session.query(Role).filter_by(character_name = "Hamlet").first()
# print(hamlet_query.actors())



