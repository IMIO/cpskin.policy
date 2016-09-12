*** Settings ***
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  plone.app.robotframework.keywords.Debugging
Library  Selenium2Screenshots

Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Test cases ***

Concept
    Go to  ${PLONE_URL}
    Page should contain  Site réalisé en collaboration
    Capture and crop page screenshot  doc/3-1 thèmes.png  id=top-search-logo  id=top-navigation


*** Keywords ***
Suite Setup
    Open test browser
    Enable autologin as  Manager
    Set Window Size  1280  800
    Set Suite Variable  ${CROP_MARGIN}  0
