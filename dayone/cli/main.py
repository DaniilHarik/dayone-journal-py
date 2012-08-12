
import baker

import dayone.journal

@baker.command
def ls():
    j = dayone.journal.Journal()
    count = 0
    for entry in reversed(j.entries_by_date()):
        t = entry.text[:40].replace("\n"," ")
        print "%4d : %s : %s : %s" % (count, entry.uuid, entry.date, t)
        count = count + 1
        

@baker.command
def show(entry):
    j = dayone.journal.Journal()
    
    if len(entry) < 32:
        entries = list(reversed(j.entries_by_date()))
        e = entries[int(entry)]
    else:
        e = j.get(entry)

    print "Entry ID: ", e.uuid
    print "Date    : ", e.date
    print "Starred : ", e.starred
    print ""
    print e.text

    
        
