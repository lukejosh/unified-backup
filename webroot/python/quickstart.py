#!/usr/bin/env python

print "Content-type: text/html\n\n"

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import pdb


def getAuthAndDrive():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")
    drive = GoogleDrive(gauth)

    return gauth, drive


def getDriveFiles(drive):
    drive_files = []
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for afile in file_list:
        drive_files.append(afile['title'])
    return drive_files


def getUploadFiles():
    upload_files = os.listdir("/home/pi/unified-backup/webroot/uploads")
    return upload_files


def uploadNew(drive_files, upload_files, drive):
    pushed_files = []
    for afile in upload_files:
        if afile not in drive_files:
            new_file = drive.CreateFile()
            new_file.SetContentFile("/home/pi/unified-backup/webroot/uploads/{0}".format(afile))
            new_file['title'] = afile
            new_file.Upload()
            pushed_files.append(afile)
    return pushed_files


def deleteUploaded(pushed_files):
    for i in pushed_files:
        os.remove('/home/pi/unified-backup/webroot/uploads/{0}'.format(i))


def main():
    gauth, drive = getAuthAndDrive()
    drive_files = getDriveFiles(drive)
    upload_files = getUploadFiles()
    pushed_files = uploadNew(drive_files, upload_files, drive)
    deleteUploaded(pushed_files)

main()
