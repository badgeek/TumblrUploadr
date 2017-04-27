#!/usr/bin/python
import pytumblr
import sys
import os

os.environ['GTK2_RC_FILES'] = "/usr/share/themes/Clearlooks/gtk-2.0/gtkrc"

from PIL import Image
from resizeimage import resizeimage
import argparse
from gooey import Gooey, GooeyParser

from private_auth import auth_key

client = pytumblr.TumblrRestClient(auth_key[0],auth_key[1],auth_key[2],auth_key[3])


print "This is the name of the script: ", sys.argv[0]
print "Number of arguments: ", len(sys.argv)
print "The arguments are: " , str(sys.argv)

def asciiart():
  print("      ,\/|         _.--''^``-...___.._.,;");
  print("     \/, \'.     _-'          ,--,,,--'''");
  print("    { \    `_-''       '    \/}");
  print("     `;;'            ;   ; ;");
  print(" ._.--''     ._,,, _..'  .;.'");
  print("  (,_....----'''     (,..--''");

@Gooey(program_name="TumblrUploadr")
def main():
  parser = GooeyParser(description='Tumblr Uploadr for Bondut.')

  selected_files = ':'.join('{0}'.format(w) for w in sys.argv[1:])


  tumblr_blog_select = []

  tumblr_blogs = client.info()['user']['blogs']
  for blog in tumblr_blogs:
    tumblr_blog_select.append(blog['name'])


  parser.add_argument(
    'tumblr_blog',
    metavar='Select Blog',
	choices= tumblr_blog_select
    )


  parser.add_argument(
    'tumblr_photos',
    metavar='Photos',
	default= selected_files,
    widget="MultiFileChooser",
    nargs="+")


  parser.add_argument(
    'tumblr_post_status',
    metavar='Post Status',
    default='draft',
	choices= ['published', 'draft', 'queue', 'private']
    )

  parser.add_argument(
    '-tumblr_tags',
    metavar='Tags',
	default= '',
    help='separated by space')


  parser.add_argument(
    '-tumblr_desc',
    metavar='Description',
	default= '',
    help='Enter Description')


  parser.add_argument(
    'tumblr_resize_width',
    metavar='Resize Width',
    default='none',
	choices= ['1280', '890', '860', '640', 'none']
    )




  args = parser.parse_args()
  print 'Hooray!'
  
  tumblr_photos = args.tumblr_photos
  tumblr_tags = args.tumblr_tags.split(' ')
  tumblr_desc = args.tumblr_desc
  tumblr_blog = args.tumblr_blog
  tumblr_state = args.tumblr_post_status
  tumblr_resize = args.tumblr_resize_width

  tumblr_photos_resized = []
  tumblr_photos_tobedeleted = []

   
  if len(tumblr_photos) > 0:
    print "Tumblr uploader. will upload " + str(len(tumblr_photos)) + " photos"
    if tumblr_resize != 'none':
      for photo_resize_file in tumblr_photos:
        resized_image_filename = photo_resize_file + ".resized"
        fd_img = open(photo_resize_file, 'r')
        img = Image.open(fd_img)
        print "---------"
        print "analyze " + photo_resize_file + " width: " + str(img.width) + " height:" + str(img.height)
        if img.width > int(tumblr_resize):
          img = resizeimage.resize_width(img, int(tumblr_resize))
          img.save(resized_image_filename, img.format)          
          tumblr_photos_resized.append(resized_image_filename)
          tumblr_photos_tobedeleted.append(resized_image_filename)
          print "resized file to " + resized_image_filename 
        else:
          tumblr_photos_resized.append(photo_resize_file)
          print "image not resized " + photo_resize_file        
        fd_img.close()
      print 'Uploading... please..wait..'        
      print tumblr_photos_resized
      client.create_photo(tumblr_blog, state=tumblr_state, tags=tumblr_tags, data=tumblr_photos_resized, caption=tumblr_desc)
      for photo_delete in tumblr_photos_tobedeleted:
        os.remove(photo_delete)
    else:      
      print 'Uploading... please..wait..'        
      client.create_photo(tumblr_blog, state=tumblr_state, tags=tumblr_tags, data=tumblr_photos, caption=tumblr_desc)    
    print 'Horeee bondut ngupload tumblr!'
    asciiart()
  else:
    print 'No Photos selected!'

if __name__ == '__main__':
   main()
