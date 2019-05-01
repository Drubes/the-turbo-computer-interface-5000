#!/usr/bin/python
################################################################################
#  Draws heath and mana orbs on you screen reprecenting free CPU and RAM.
#
#  PART OF "THE TURBO COMPUTER INTERFACE 5000"
#  As seen on: https://consolia-comic.com/comics/interface
#                                shoutout to Wiskybaard!!!!
#
#
#  Images are borrowed (without premission) of screenshots from diablo II,
#  I hope they see this work as fan-art and that they won't sue me.
#
#  This script is licensed under the Creative Commons Attribution 4.0
#  International License. To view a copy of this license,
#  visit http://creativecommons.org/licenses/by/4.0/ or send a letter to
#  Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
#
#  Date   : 02-05-2019
#  Author : Robert McCallum
#           http://robertmccallum.nl
#
################################################################################
#
#  Usage:  just run the script and enjoy.
#          to close.. just kill it.
#
################################################################################

import math
from gi.repository import Gtk, Gdk, GObject
import cairo
import psutil

class bawls(Gtk.Window):
    def __init__(self, name):
        self.name = name
        Gtk.Window.__init__(self, type=Gtk.WindowType.POPUP)
        self.screen = self.get_screen()
        self.workarea = self.screen.get_monitor_workarea(0)
        self.visual = self.screen.get_rgba_visual()
        if self.visual != None and self.screen.is_composited():
            self.set_visual(self.visual)
        else:
            print "sorry, no transparency for you!!\n"\
                  "update gtk or something,\n"\
                  "change your settings,\n"\
                  "fix this script,\n"\
                  "get your shit sorted..\n"
        self.set_app_paintable(True)
        self.connect("draw", self.area_draw)
        self.init_ui()
        self.ticker()


    def init_ui(self):
        self.darea = Gtk.DrawingArea()
        darea = self.darea
        darea.set_size_request(76,76)
        self.workarea = Gdk.Screen.get_monitor_workarea(self.screen,0)
        if self.name=="mana":
            self.move(self.workarea.width-106, self.workarea.height-90)
            #self.move(1172, 905)
            darea.connect("draw", self.mana_draw)
        if self.name=="health":
            #self.move(32, 905)
            self.move(32,self.workarea.height-90)
            darea.connect("draw", self.health_draw)
        self.add(darea)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


    def mana_draw(self, wid, cr):
        x =  (psutil.cpu_percent() /100)
        cr.arc(38, 38, 38, 0, 2*math.pi)
        lg = cairo.LinearGradient(38, 0, 38, 76)
        lg.add_color_stop_rgba(0, 0, 0, 0, 0)
        lg.add_color_stop_rgba(x-0.1, 0, 0, 0, 0)
        lg.add_color_stop_rgba(x, 0, 0, 0.8, 1)
        lg.add_color_stop_rgba(1, 0, 0, 1, 1)
        cr.set_source(lg)
        cr.fill()

    def health_draw(self, wid, cr):
        x =  (psutil.virtual_memory()[2] /100)
        cr.arc(38, 38, 38, 0, 2*math.pi)
        lg = cairo.LinearGradient(38, 0, 38, 76)
        lg.add_color_stop_rgba(0, 0, 0, 0, 0)
        lg.add_color_stop_rgba(x-0.1, 0, 0, 0, 0)
        lg.add_color_stop_rgba(x, 0.5, 0, 0, 1)
        lg.add_color_stop_rgba(1, 1, 0, 0, 1)
        cr.set_source(lg)
        cr.fill()

    def update_fill(self):
        self.queue_draw()
        return True

    def area_draw(self, widget, cr):
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

    def ticker(self):
        GObject.timeout_add(1000, self.update_fill)


class overlay(Gtk.Window):
    def __init__(self, name):
        self.name = name
        Gtk.Window.__init__(self, type=Gtk.WindowType.POPUP)
        self.screen = self.get_screen()
        self.workarea = Gdk.Screen.get_monitor_workarea(self.screen,0)
        self.image = Gtk.Image()
        self.image.set_from_file(self.name+".png")
        self.add(self.image)
        self.visual = self.screen.get_rgba_visual()
        if self.visual != None and self.screen.is_composited():
            self.set_visual(self.visual)
        self.set_app_paintable(True)
        self.connect("draw", self.area_draw)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        if self.name == "mana":
            self.move(self.workarea.width-self.get_allocated_width(), self.workarea.height-self.get_allocated_height())
        if self.name == "health":
            self.move(0, self.workarea.height-self.get_allocated_height())

    def area_draw(self, widget, cr):
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

def main():
    h = bawls("health")
    m = bawls("mana")
    ho = overlay("health")
    mo = overlay("mana")
    Gtk.main()

if __name__ == "__main__":
    main()
