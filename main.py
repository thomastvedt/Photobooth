# -*- coding: iso-8859-1 -*-
# A simple photobooth for my wedding
# Hardcoded resolution: 4:3, 1280x1024

from time import sleep
import os
import os.path
import subprocess as sub
import datetime
import pygame
import sys
import math
import shutil
from PIL import Image

width = 1280
height = 1024
color_white = pygame.Color(255,255,255)
color_black = pygame.Color(0,0,0)
color_pink = pygame.Color(175,50,55)
color_mint = pygame.Color(12,145,44)

print "Starting amazing photobooth..."
pygame.init()
pygame.display.set_caption("Photobooth")

screen = pygame.display.set_mode((width,height))#NOT FULLSCREEN
#screen = pygame.display.set_mode((width,height),pygame.FULLSCREEN)#FULLSCREEN
clock = pygame.time.Clock()
game_isrunning = True
img_ready = pygame.image.load("ready.jpg")
img_capture = pygame.image.load("capture.jpg")
img_working = pygame.image.load("working.jpg")
img_finished = pygame.image.load("finished.jpg")
img_last_collage_small = pygame.image.load("preview.jpg")
img_last_collage_full = pygame.image.load("finished.jpg")
img_monogram = pygame.image.load("monogram2.jpg")
img_cap1 = pygame.image.load("1.jpg")
img_cap2 = pygame.image.load("2.jpg")
img_cap3 = pygame.image.load("3.jpg")
img_cap4 = pygame.image.load("4.jpg")

rect_full = img_ready.get_rect()
rect_cap1 = img_cap1.get_rect()
rect_cap2 = img_cap2.get_rect()
rect_cap3 = img_cap3.get_rect()
rect_cap4 = img_cap4.get_rect()
rect_cap1.x = 55
rect_cap2.x = 57
rect_cap3.x = 57
rect_cap4.x = 57
rect_cap1.y = 32
rect_cap2.y = 280
rect_cap3.y = 531
rect_cap4.y = 779
rect_last_collage_small = img_last_collage_small.get_rect()
rect_last_collage_small.x = 668
rect_last_collage_small.y = 363
rect_last_collage_full = img_last_collage_full.get_rect()
rect_last_collage_full.x = 0
rect_last_collage_full.y = 0
game_state = "ready"
game_count_captures = 0
game_count_captures_ok = 0
game_wait_for_capture = False
game_wait_ms = 0
p1 = None
cap_cooldown = 6700
cap_last = None
cap_guid = "na"
preview_timer = 10000
preview_last = None

def GetDateTimeString():
    #format the datetime for the time-stamped filename
    dt = str(datetime.datetime.now()).split(".")[0]
    clean = dt.replace(" ","_").replace(":","_")
    return clean

try:
    while game_isrunning:
        spent_ms = clock.tick(50)

        #input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print "pygame.QUIT-event detected"
                game_isrunning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print "Escape pressed, quiting.."
                    game_isrunning = False
                if event.key == pygame.K_SPACE:                    
                    if game_state == "ready":
                        print "SET state to capture.."
                        game_state = "capture"
                        game_count_captures = 0
                        game_count_captures_ok = 0
                        game_wait_for_capture = False
                        game_wait_ms = 0
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print pos

        #logic
        if game_state == "ready":
            screen.blit(img_ready,rect_full)            
        elif game_state == "capture":
            if game_wait_for_capture == True:
                temp_img_name = "cap_%s.jpg" % game_count_captures
                if game_count_captures > game_count_captures_ok:   
                    #new test: wait for cooldown. . .
                    now = pygame.time.get_ticks()
                    if now - cap_last >= cap_cooldown:                    
                        print "load img %s.." % temp_img_name
                        capture_src = pygame.image.load(temp_img_name)
                        dest_name = "originals/cap_%s_%s" % (cap_guid, game_count_captures)
                        print "copy from SRC %s to DEST %s" % (temp_img_name, dest_name)
                        shutil.copyfile(temp_img_name, dest_name)

                        #small boxes: 286x214
                        capture_resized = pygame.transform.scale(capture_src.convert_alpha(),(286,214))

                        if game_count_captures == 1:
                            img_cap1 = capture_resized
                        elif game_count_captures == 2:
                            img_cap2 = capture_resized
                        elif game_count_captures == 3:
                            img_cap3 = capture_resized
                        elif game_count_captures == 4:
                            img_cap4 = capture_resized
                                            
                        print "great success!"
                        game_count_captures_ok = game_count_captures_ok + 1
                        game_wait_for_capture = False
                        print "game_count_captures: %s game_count_captures_ok: %s" %(game_count_captures,game_count_captures_ok)
                    else:
                        print "cool down..."
            else: # TAKE PICTURE!
                if game_count_captures == game_count_captures_ok and game_count_captures < 4:
                    print "firing capture command and waiting..."
                    game_wait_for_capture = True
                    game_count_captures = game_count_captures + 1
                    cap_last = pygame.time.get_ticks()
                    cap_cooldown = 6700
                    temp_cmd = "raspistill -p 494,282,706,521 -o cap_%s.jpg" % game_count_captures
                    cap_guid = GetDateTimeString()
                    print "cap_guid:%s" % cap_guid
                    p1 = sub.Popen(temp_cmd, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
                else:
                    print "next step.."
                    game_state = "working"
        elif game_state == "working":
            print "working"
            #minihack: update gfx here..
            screen.blit(img_working,rect_full)
            pygame.display.flip()

            #Assemble 4 pictures into 1 using a template
            print "open images..."
            template = Image.open("template2.jpg")
            thumb1 = Image.open("cap_1.jpg")
            thumb2 = Image.open("cap_2.jpg")
            thumb3 = Image.open("cap_3.jpg")
            thumb4 = Image.open("cap_4.jpg")
            #thumb1.thumbnail((435,326))
            #template = 1280x1024, thumbs = 435x326, src = 2900x??? 5MP
            #template2 = 2560x2048
            print "creating thumbnails..."
            thumb1.thumbnail((870,652))
            thumb2.thumbnail((870,652))
            thumb3.thumbnail((870,652))
            thumb4.thumbnail((870,652))
            print "pasting..."
            template.paste(thumb1, (200, 434))
            template.paste(thumb2, (1240, 434))
            template.paste(thumb3, (200, 1200))
            template.paste(thumb4, (1240, 1200))            
            collage_dest = "assembled/collage_%s.jpeg" % cap_guid
            print "Saving to: %s" % collage_dest
            template.save(collage_dest)
            print "save OK: %s" % collage_dest
            print "load last collage into preview..."
            img_last_collage_SRC = pygame.image.load(collage_dest)
            img_last_collage_full = pygame.transform.scale(img_last_collage_SRC.convert_alpha(),(1280,1024))
            rect_last_collage_full = img_last_collage_full.get_rect()
            rect_last_collage_full.x = 0 #668
            rect_last_collage_full.y = 0 #363            
            print "ASDF2:%s" % rect_last_collage_full.width
            img_last_collage_small = pygame.transform.scale(img_last_collage_SRC.convert_alpha(),(433,328))

            #reset images..
            img_cap1 = pygame.image.load("1.jpg")
            img_cap2 = pygame.image.load("2.jpg")
            img_cap3 = pygame.image.load("3.jpg")
            img_cap4 = pygame.image.load("4.jpg")
            
            print "goto finished state"
            game_state = "finished"
            
            #TODO: optional print image
            preview_last = pygame.time.get_ticks()
        elif game_state == "finished":            
            now = pygame.time.get_ticks()
            if now - preview_last >= preview_timer: 
                print "preview finished..."
                game_state = "ready"
            else:
                print "showing preview.."
        #gfx
        if game_state == "ready":
            screen.blit(img_ready,rect_full)
            #lastimg: x 668, y 363, width= 433 height = 328
            screen.blit(img_last_collage_small, rect_last_collage_small)
        elif game_state == "capture":
            screen.blit(img_capture,rect_full)
            screen.blit(img_cap1, rect_cap1)
            screen.blit(img_cap2, rect_cap2)
            screen.blit(img_cap3, rect_cap3)
            screen.blit(img_cap4, rect_cap4)            
        elif game_state == "working":
            #screen.blit(img_working,rect_full)
            print "working gfx.."
        elif game_state == "finished":
            #Showing assembled picture:
            screen.blit(img_last_collage_full,rect_last_collage_full)
            
        fps = clock.get_fps()
        screen.blit(pygame.font.SysFont("freeserif",20,bold=0).render("{0:.2f}".format(fps) + " fps", 1, color_black),((width - 20),10))
        pygame.display.flip() # or update()?

    print "Loop finished.."
except Exception, e:
    print "An error occured.."
    tb = sys.exc_info()[2]
    print "ERROR CLASS:%s" % e.__class__
    print "ERROR MSG:  %s" % e
    
finally:
    print "pygame quit.."
    #This line makes debugging much easier
    pygame.quit()

print "Script finished"
