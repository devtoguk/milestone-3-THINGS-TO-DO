# Things To Do Places To Go - Testing Information

[Live app deployed on Heroku](https://things-to-do-project.herokuapp.com/)

[Back to main README.md file](/README.md)

## Table of Contents
- [Software Tools](#software-tools)
- [User story testing](#user-story-testing)
- [Testing elements and functionality of the project](#testing-elements-and-functionality-of-the-project)
- [Additional Testing](#additional-testing)
- [Errors and Issues Found](#errors-and-issues-found)

## Software Tools
- [JSHint - Code Analysis Tool](https://jshint.com/) - used to help detect errors and potential problems in JavaScript code.
- [W3C - Markup Validation Service](https://validator.w3.org/) - used to check the markup validity of the HTML documents.  However some errors were shown due to the presence of the Jinja template language.
- [W3C - CSS Validation Service](https://jigsaw.w3.org/css-validator/) - used to check the validity of the Cascading Style Sheets (CSS).
  Had several Parse Errors but these seem to be caused by my use of CSS variables. Found the following link which explained more why I
  got the errors. [Stackoverflow](https://stackoverflow.com/questions/57661659/w3c-css-validation-parse-error-on-variables)
- [Flake8 within GitPod]() - used to check Python code base against coding style (PEP8)
- [Chrome Developer Tools](https://developers.google.com/web/tools/chrome-devtools) - used to help check the responsiveness of the app and also use of Audits to test for performance, accessibility, best practices & SEO

## User story testing

### Customer
1. How do I search for activities using a word or phrase?

    1. The user would go to the Home page.
    2. Enter their search word or phrase into the text input and press the [Search] button.
    3. A message will be displaying showing how many results were found and what 'word/phrase' they used. If no results are found then a message indicating this will be displayed.
    4. The results of the users search will be displayed as activity cards which the user can click on to see further details about an activity.

2. How do I find activities by category.

    1. From the navigation bar the user can choose the 'Activities' drop-down menu.
    2. From this menu select one of the categories to find activities that match.
    3. A message will be displaying showing how many results were found and what [Category] they selected. If no results are found then a message indicating this will be displayed.
    4. The results of the users search will be displayed as activity cards which the user can click on to see further details about an activity.

3. How can I submit my own idea for an activity.

    1. To submit an activity the user must be logged-in.
    2. Once logged-in, the user would click on the navigation item 'Submit Activity'.
    3. When adding an activity you DO NOT have to choose an image straight-away, this can be added later if you do not have an image to hand. A 'picture not available' image will be displayed for the activity.
    4. Complete the 'Add an Activity' form and click [Add Activity].
    5. If there are any validation errors the user should correct these and click [Add Activity]

4. How can I see all the activities I have submitted.

    1. The user must be logged-in to view a list of all activities they have submitted.
    2. To view a list of all the activities they have submitted a user can select the 'Submitted by Me' option from the profile menu.
    3. The list will be displayed as activity cards which the user can click on to see further details about the activity.

5. How can I edit an activity I have submitted.

    1. To edit an activity the user must be logged-in.
    2. Also a user must either have originally submitted the activity or be an admin/moderator to be able to edit an activity.
    3. On an activity card, the user should click on the [Edit] button.
    4. The 'Edit Activity' form is displayed and the user can now edit the required fields and then click [Update Activity].
    5. If there are any validation errors the user should correct these and click [Update Activity].

6. How do I find featured activities.

    1. From the navigation bar the user can choose the 'Activities' drop-down menu.
    2. From this menu select 'Featured'.
    3. A message will be displaying showing 'Featured Activities'.
    4. The results of the 'Featured' search will be displayed as activity cards which the user can click on to see further details about an activity.

7. How do I find newly added activities.

    1. From the navigation bar the user can choose the 'Activities' drop-down menu.
    2. From this menu select 'Recently Added'.
    3. A message will be displaying showing 'Recently Added Activities'.
    4. The results of the 'Recently Added' search will be displayed as activity cards which the user can click on to see further details about an activity.  (Note: only the most recent 6 activities created will be shown)

8. How do I keep a list of my favourite activities.

    1. To keep track of your favourite activities a user must be logged-in.
    2. When viewing the full details of an activity the user can use the 'heart-icon' in the top-right of the activity view to either add or remove the activity from their 'Favourite Activities' list.
    3. To view your Favourite Activity list a user can select 'My Favourites' option from the profile menu. The list will be displayed as activity cards which the user can click on to see further details about the activity.

### Administrator
( to test use login: adrian@ttdaptg.com !!-print(Check)! )
1. How do I approve or disapprove user submitted activities.
    1. Due to time constraints only the visible menu option for this function exists in the user 'Profile' menu, it is only visible when logged-in as an 'admin'.
2. How do I maintain existing users.
    1. Due to time constraints only the visible menu option for this function exists in the user 'Profile' menu, it is only visible when logged-in as an 'admin'.
3. Ability to edit any activity record.
    1. To edit any activity the 'admin' user must be logged-in.
    2. On any activity card, the 'admin' user should see and be able to click on the [Edit] button.
    3. The 'Edit Activity' form is displayed and the 'admin' user can now edit the required fields and then click [Update Activity].
    4. If there are any validation errors the 'admin' user should correct these and click [Update Activity].

### Advertiser
1. How do I get my banner on the app?
    1. Due to time constraints this will now be part of our future development, as the app gets more popular.
2. How can I find out how many clicks my banner has received.
    1. Due to time constraints this will now be part of our future development, as the app gets more popular.

## Testing elements and functionality of the project
(manual tests)

### General
- Make sure that all app pages display as they should.
- Ensure that the logo and navigation display correctly on different device screen sizes.
- Check that all navigation and logo links are working.
- Check that the alt/title text appears on the logo image.
- Ensure that font sizes are readable on different devices.
- Check that footer social links are working.

### Home page
1. Check the search text input works and the [Search] button functions.
2. Check expected search results.

### About page
1. Check that the text displays correctly
2. Ensure that the DB stats are correct.

### Activities (menu)
1. Check that the menu displays as it should on all devices.
2. Ensure each menu option (All, Featured, Recently Added, Animals, Attraction, Crafting, Food, Nature, Sport and Leisure) give the expected results.

### Submit/Edit an Activity
1. Confirm all the input fields work as expected and the [Add Activity] button functions and displays processing indicator.
2. Confirm that an 'admin' user can edit any activity.
3. Check client and server side form validation is working as expected.
4. Check [x] link in the top-right allows the user to abort the submit/edit.

### Login/Register
1. Check the email and password input fields work and the [Login] button functions and a user can actually be logged-in.
2. Check the [Register] button takes the user to the 'User Registration'.
3. At 'User Registration' confirm all the input fields work as expected and the [Register] button functions.
4. Check that a user actually gets registered.
5. Check the 'HERE' to login link works.

### Profile (menu)
1. Check that the menu displays as it should on all devices.
2. Ensure each menu option (View Profile, My Favourites, Submitted by Me, Logout) give the user the expected results.

### Displayed Results (from Activities or Profile menu options)
1. Check that the results are displayed in the correct format depending on the screen size.
2. Has the correct flash message been displayed.
3. Ensure that the image and [More Details] button link to the full activity view.
4. Check that the [Edit] button only displays if the user originally submitted the activity or the current user is an admin/moderator.
5. Confirm that the correct data has been displayed.

### Activity View
1. Check that the results are displayed in the correct format depending on the screen size.
2. Ensure that the 'Add to Activity Favourites' heart-icon works as expected.
3. Check the alt/title text changes on the heart-icon.
4. Ensure activity links work and only appear if the data is present.
5. Are the activity flag-icons correct.
6. Check the 'creator' info at the bottom of the view.
7. Confirm that the correct data has been displayed.

## Additional Testing
1. Asked friends and family to use the application on their phone, tablets and desktops where possible and let me know any issues. Got good feedback, with no real issues.
2. I have tested the app on a desktop using the following modern browsers: Chrome, Firefox and Edge. As well as testing on Android phone/tablet and Apple iPhone.
3. The application has not been written to work on Internet Explorer. In the real World if a client wanted an application to work on IE then that is fine, but a lot of the newer methods of coding Javascript, etc does not work on IE. IE has had it's day and I wanted to code the app using some of these newer methods.

## Errors and Issues Found
(only includes main errors/issues rather than easy to solve coding, typos, alignment, etc which caused only minor errors)

1. **Uploaded images on Heroku**
As far as user images on this project, I did not realise that we could just use a link rather than getting the users to actually upload images. So I did go down the route of image uploads, cropping, resizing, etc.  This all worked well while testing on GitPod, however when I deployed the app to Heroku the images no longer appeared. Other than the tutor led course material I had never used Heroku before, so was a little puzzled but after some research I realized that while the image is actually uploaded to Heroku it doesn't actually store the image for very long.  I had a decision to make, undo all the effort and coding I had done for the images or spend time to find a solution. After further investigation I discovered AWS S3 Bucket was a place for my app to upload the images to and serve them back to the users.  This took more time than I thought, but I feel it was well worth it in the end.

2. **Image cropping/resizing**
When resizing images occasionally a landscape image being resized/cropped ends up with black bars either side of the image.  Due to time constraints I have not yet had time to solve this issue.

3. **Additional location value**
During testing and data entry it became obvious that we really needed an additional value for the 'location' field to deal with activities which were 'Out & About' but did not have a specific venue.  So, 'At a Venue' was added for activities with a specific address.

4. **https:// changing to http://**
While testing on Heroku I have noticed that while the site starts off on a  secure 'https://' url, as soon as you do an activity/view it changes to a 'http://' url. Even though at the base of the browser window it clearly says it is linking to a 'https://' url.  In 'heroku logs --tail' you can see the protocol change to 'http'.
Due to time constraints I have not had the time to investigate this further yet, but think this issue could be related to the fact that I haven't specifically added an SSL certificate to my Heroku Dyno or the fact that I am not using a paid Dyno.
Either way this issue would need to be solved before going fully live.

5. **Image file-input field**
On an actual Android mobile and tablet the 'file-input' filename still overflowed, but in Google Dev Tools it does not. Performed an update for Chrome on both devices and now it works as expected on the tablet but the mobile still has the issue, further investigation is required.
