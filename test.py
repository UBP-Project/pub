from app.models import Interest_Group

def test():
    group = Interest_Group.query.first()
    print(group.name)
    print('GET LEADER')
    leaders = group.get_leaders()
    print(leaders)

    print('GET MEMBERS')
    members = group.get_members()
    print(members)

    print('GET REQUEST')
    requests = group.get_requests()
    print(requests)

    print('SET LEADER')
    print(group.set_leader(members[0].id))

    print('REMOVE LEADER')
    print(group.remove_leader(leaders[0].id))

