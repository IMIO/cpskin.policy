*** Settings ***
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot
Resource  common.robot

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
    
Créer la navigation
    Go to  ${PLONE_URL}
#    Click Element  portaltab-ma-commune
#   Wait until element is visible  ma-commune-services-communaux  10
#    Click Element  ma-commune-services-communaux
#   Wait until element is visible  ma-commune-services-communaux-informatique  10
#    Click Element  ma-commune-services-communaux-informatique
    Go to  ${PLONE_URL}/ma-commune/services-communaux/informatique
    Highlight  portal-breadcrumbs  3  solid
    Update element style  portal-breadcrumbs  margin-top  10px
    Capture and crop page screenshot  doc/3-3 création.png  id=top-navigation  id=portal-breadcrumbs  css=#content .documentFirstHeading
    Clear highlight  portal-breadcrumbs
    Update element style  portal-breadcrumbs  margin-top  0px
    Go to  ${PLONE_URL}/folder_contents
    Highlight  folder-contents-item-ma-commune  3  solid
    Capture and crop page screenshot  doc/3-3 content-état.png  id=listing-table
    Clear highlight  folder-contents-item-ma-commune


*** Keywords ***
Suite Setup
    Open test browser
    Enable autologin as  Manager
    Set Window Size  1280  800
    Set Suite Variable  ${CROP_MARGIN}  0

    
