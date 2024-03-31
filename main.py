#!/usr/bin/python3
"""
 Test cities access from a state
"""
from models import storage
from models.state import State
from models.city import City

"""
 Objects creations
"""
state_1 = State(name="California")
print("New state: {}".format(state_1))
state_1.save()
state_2 = State(name="Arizona")
print("New state: {}".format(state_2))
state_2.save()
state_3 = State(name="Alabama")
print("New state: {}".format(state_3))
state_3.save()
state_4 = State(name="Florida")
print("New state: {}".format(state_4))
state_4.save()
state_5 = State(name="Georgia")
print("New state: {}".format(state_5))
state_5.save()
state_6 = State(name="Hawaii")
print("New state: {}".format(state_6))
state_6.save()
state_7 = State(name="Illinois")
print("New state: {}".format(state_7))
state_7.save()
state_8 = State(name="Indiana")
print("New state: {}".format(state_8))
state_8.save()
state_9 = State(name="Mississippi")
print("New state: {}".format(state_9))
state_9.save()
state_10 = State(name="Louisiana")
print("New state: {}".format(state_10))
state_10.save()


city_1_1 = City(state_id=state_1.id, name="Napa")
print("New city: {} in the state: {}".format(city_1_1, state_1))
city_1_1.save()
city_1_2 = City(state_id=state_1.id, name="Sonoma")
print("New city: {} in the state: {}".format(city_1_2, state_1))
city_1_2.save()
city_2_1 = City(state_id=state_2.id, name="Page")
print("New city: {} in the state: {}".format(city_2_1, state_2))
city_2_1.save()


"""
 Verification
"""
print("")
all_states = storage.all(State)
for state_id, state in all_states.items():
    for city in state.cities:
        print("Find the city {} in the state {}".format(city, state))
