clean_links = [1,2,3]
image_site_map = [1,2,3]
# test = {"site_map":clean_links, "image_site_map":image_site_map}
data = {'site_map':clean_links, 'image_site_map':image_site_map}
for key, clean_links in {'site_map':clean_links, 'image_site_map':image_site_map}.items():
    print(key)
    for each in clean_links:
        print(each)