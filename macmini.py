import osxphotos
import datetime
import os
import shutil

from datetime import date, timedelta
from exif import Image

from wand.image import Image

def main():


    # This is yesterday's date - relevant for daily exports
    today = date.today()
    yesterday = today - timedelta(days = 1)
    yes_str = yesterday.strftime('%Y%m%d')
    yes_year = yesterday.strftime('%Y')
    yes_month = yesterday.strftime('%m')
    yes_day = yesterday.strftime('%d')

    # Start exporting photos from this date onwards
    yes_str = '20201101'

    photosdb = osxphotos.PhotosDB()
    photos = photosdb.photos(from_date=datetime.datetime.strptime(yes_str, '%Y%m%d'))


    for p in photos:
        if not p.shared or p.shared == None:
        # The folder structure - right now it is root / year / month
            # if hasattr(p.exif_info, 'camera_model'):
            #     fold_struc = "export/%Y/%m/" + str(p.exif_info.camera_model)
            # else:
            fold_struc = 'export/%Y/%m/'
            fold_struc_mov = 'export/%Y/%m/movies/'
            fold_struc_no_model='export/%Y/%m/none/'

            prep_dir = 'export/tmp'

            os.makedirs(p.date.strftime(fold_struc_mov), exist_ok=True)
            mov_dir = p.date.strftime(fold_struc_mov)
            os.makedirs(p.date.strftime(prep_dir), exist_ok=True)
            prep_dir_str = p.date.strftime(prep_dir)
            
           
            new_name = p.date.strftime('%Y%m%d') + '_' + p.original_filename

            if p.ismovie:
                p.export(mov_dir, p.date.strftime('%Y%m%d') + '_' + p.original_filename)
            else:
                if p.hasadjustments:
                    p.export(p.date.strftime(prep_dir), p.date.strftime('%Y%m%d') + '_' + p.original_filename, edited=True)
                else:
                    p.export(p.date.strftime(prep_dir), p.date.strftime('%Y%m%d') + '_' + p.original_filename)

            if not p.ismovie:
                basepath = prep_dir
                with open(basepath + '/' + new_name, 'rb') as image_file:
                    my_image = Image(image_file)
                    # print(my_image.model)
                    try:
                        fold_struc = fold_struc + my_image.model
                        os.makedirs(p.date.strftime(fold_struc), exist_ok=True)
                        tar_dir = p.date.strftime(fold_struc) + '/'
                        shutil.move(prep_dir_str + '/' + new_name, tar_dir)
                    except AttributeError:
                        os.makedirs(p.date.strftime(fold_struc_no_model), exist_ok=True)
                        tar_dir = p.date.strftime(fold_struc) + 'none/'
                        shutil.move(prep_dir_str + '/' + new_name, tar_dir)

            # if not p.ismovie:
            #     basepath = prep_dir
            #     with os.scandir(basepath) as entries:
            #         for entry in entries:
            #             if entry.is_file():
            #                 # print(entry.name)
            #                 with open(entry, 'rb') as image_file:
            #                     my_image = Image(image_file)
            #                     # print(my_image.model)
            #                     fold_struc = fold_struc + my_image.model
            #                     os.makedirs(p.date.strftime(fold_struc), exist_ok=True)
            #                     tar_dir = p.date.strftime(fold_struc) + '/'
            #                     shutil.move(prep_dir_str + '/' + new_name, tar_dir)

            # print(
            #       p.original_filename)
            #     p.shared,
            #     p.exif_info.camera_model,
            #     # p.path_edited,
            #     # p.path,
            #     p.hasadjustments
            #     # p.date.strftime('%Y%m%d'),
            #     # file_extension,
            #     # p.date.strftime('%Y%m%d') + str(file_extension)
            # )


if __name__ == "__main__":
    main()
