#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from selenium import webdriver
import os

class Singleton(object):

    instance = None


    def __new__(cls, browser='ie'):
        IEdriver = "C:\Program Files (x86)\Internet Explorer\IEDriverServer.exe"

        if cls.instance is None:
            i = object.__new__(cls)
            cls.instance = i
            cls.browser = browser

            if browser == "ie":
                os.environ["webdriver.ie.driver"] = IEdriver
                cls.driver = webdriver.Ie()
                # Create a new instance of the Firefox driver
            elif browser == "remote":
                # Create a new instance of the Chrome driver
                cls.driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNITWITHJS)
            else:
                # Sorry, we can't help you right now.
                #asserts.fail("Support for Firefox or Remote only!")
                pass

        else:

            i = cls.instance

        return i
