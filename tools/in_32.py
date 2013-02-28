# In-16
sdoc = params["input"]
tdoc = params["output"]

#crops_mark = params['cr']

dep = int(params["d"])


t0 = [
    [60,5,12,53,56,9,8,57],
    [-37,-28,-21,-44,-41,-24,-25,-40],
    [36,29,20,45,48,17,32,33],
    [-61,-4,-13,-52,-49,-16,-1,-64]
    ]

t1 = [
    [62,3,14,51,50,15,2,63],
    [-35,-30,-19,-46,-47,-18,-31,-34],
    [38,27,22,43,42,23,26,39],
    [-59,-6,-11,-54,-55,-10,-7,-58]
    ]

sinfo = pdf_info.extract(sdoc)
bbox = sinfo["page_size"][0][1]
pcount = sinfo["page_count"]
swidth = bbox["width"]
sheight = bbox["height"]


hor_extra = 0
vert_extra = 0
twidth = 8 * swidth
theight = 4 * sheight
#twidth = 2891.3386
#theight = 1984.252


x_offset = 0 #(twidth - (8*swidth)) / 2.0
y_offset = 0 #(theight - (4*sheight)) / 2.0

imposition_plan = []
recto_pages = []
verso_pages = []

### recto ################################


for py in [0,1,2,3]:
    for px in [0,1,2,3,4,5,6,7]:
        rotate = False
        source_page = t0[py][px] * 1
        if source_page < 0:
            rotate = True
            source_page *= -1
        x = (px * swidth) + x_offset
        y = (py * sheight) + y_offset
        r = 0
        if rotate:
            r = 180
            x += swidth
            y += sheight
            
        if pcount > (source_page - 1 + dep):
            recto_pages.append({
                    "source_document" : sdoc,
                    "source_page" : source_page - 1 + dep,
                    "crop_box" : {"left":0,"bottom":0,"width":swidth, "height":sheight},
                    "translate" : [x,y],
                    "rotate" : r,
                    "scale" : [1,1]
                    })
                
#for py in [0,1,2,3]:
    #for px in [0,1,2,3,4,5,6,7]:
        #rotate = False
        #source_page = t0[py][px] * 1
        #if source_page < 0:
            #rotate = True
            #source_page *= -1
        #x = (px * swidth) + x_offset + (4 * swidth)
        #y = (py * sheight) + y_offset
        #r = 0
        #if rotate:
            #r = 180
            #x += swidth
            #y += sheight
        #if pcount > (source_page - 1+ 32 + dep):
            #recto_pages.append({
                    #"source_document" : sdoc,
                    #"source_page" : source_page - 1 + 32 + dep,
                    #"crop_box" : {"left":0,"bottom":0,"width":swidth, "height":sheight},
                    #"translate" : [x,y],
                    #"rotate" : r,
                    #"scale" : [1,1]
                    #})

                    
#recto_pages.append({
                    #"source_document" : crops_mark,
                    #"source_page" : 0,
                    #"crop_box" : {"left":0,"bottom":0,"width":twidth, "height":theight},
                    #"translate" : [0,0],
                    #"rotate" : 0,
                    #"scale" : [1,1]
                    #})
imposition_plan.append({
            "target_document" : tdoc,
            "target_page_width" : twidth,
            "target_page_height" : theight,
            "pages": recto_pages})
                
                

### end of recto ################################

### verso ################################
#for py in [0,1,2,3]:
    #for px in [0,1,2,3]:
        #rotate = False
        #source_page = t1[py][px] * 1
        #if source_page < 0:
            #rotate = True
            #source_page *= -1
        #x = (px * swidth) + x_offset + (4 * swidth)
        #y = (py * sheight) + y_offset
        #r = 0
        #if rotate:
            #r = 180
            #x += swidth
            #y += sheight
        #if pcount > (source_page - 1 + dep):
            #verso_pages.append({
                    #"source_document" : sdoc,
                    #"source_page" : source_page - 1 + dep,
                    #"crop_box" : {"left":0,"bottom":0,"width":swidth, "height":sheight},
                    #"translate" : [x,y],
                    #"rotate" : r,
                    #"scale" : [1,1]
                    #})
                
#for py in [0,1,2,3]:
    #for px in [0,1,2,3]:
        #rotate = False
        #source_page = t1[py][px] * 1
        #if source_page < 0:
            #rotate = True
            #source_page *= -1
        #x = (px * swidth) + x_offset 
        #y = (py * sheight) + y_offset
        #r = 0
        #if rotate:
            #r = 180
            #x += swidth
            #y += sheight
        #if pcount > (source_page - 1+ 32 + dep):
            #verso_pages.append({
                    #"source_document" : sdoc,
                    #"source_page" : source_page - 1 + dep + 32,
                    #"crop_box" : {"left":0,"bottom":0,"width":swidth, "height":sheight},
                    #"translate" : [x,y],
                    #"rotate" : r,
                    #"scale" : [1,1]
                    #})
#verso_pages.append({
                    #"source_document" : crops_mark,
                    #"source_page" : 0,
                    #"crop_box" : {"left":0,"bottom":0,"width":twidth, "height":theight},
                    #"translate" : [0,0],
                    #"rotate" : 0,
                    #"scale" : [1,1]
                    #})
#imposition_plan.append({
            #"target_document" : tdoc,
            #"target_page_width" : twidth,
            #"target_page_height" : theight,
            #"pages": verso_pages})
                
### end of verso ################################

