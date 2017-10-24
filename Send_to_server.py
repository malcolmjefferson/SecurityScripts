   # dirlist on remote host
#    dirlist = sftp.listdir('.')
#    print "Dirlist:", dirlist
#    Change from copying file to server to copying file from server to host. 
    try:
        sftp.mkdir(dir_remote)
    except IOError, e:
        print '(assuming ', dir_remote, 'exists)', e

#    print 'created ' + dir_remote +' on the hostname'

    # BETTER: use the get() and put() methods
    # for fname in os.listdir(dir_local):

    for fname in glob.glob(dir_local + os.sep + glob_pattern):
        is_up_to_date = False
        if fname.lower().endswith('xml'):
            local_file = os.path.join(dir_local, fname)
            remote_file = os.path.dirname(fname) + '/' + dir_remote

            #if remote file exists
            try:
                if sftp.stat(remote_file):
                    local_file_data = open(local_file, "rb").read()
                    remote_file_data = sftp.open(remote_file).read()
                    md1 = md5.new(local_file_data).digest()
                    md2 = md5.new(remote_file_data).digest()
                    if md1 == md2:
                        is_up_to_date = True
                        print "UNCHANGED:", os.path.basename(fname)
                    else:
                        print "MODIFIED:", os.path.basename(fname),
            except:
                print "NEW: ", os.path.basename(fname),

            if not is_up_to_date:
                print 'Copying', remote_file, 'to ', local_file
                sftp.get(remote_file, local_file)
                files_copied += 1
    t.close()

except Exception, e:
    print '*** Caught exception: %s: %s' % (e.__class__, e)
    try:
        t.close()
    except:
        pass
