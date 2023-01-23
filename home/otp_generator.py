import uuid 


# Generating random transaction id using uuid1()
def meetingID():
    from home.models  import Meeting
    
    new_id = str(uuid.uuid1())
    print(new_id)
    all_meeeting_id = Meeting.objects.all()
    if Meeting.objects.all().count() == 0:
        return new_id
    else:
        for item in all_meeeting_id:
            if item.meeting_id == new_id:
                meetingID()
            else:
                return new_id