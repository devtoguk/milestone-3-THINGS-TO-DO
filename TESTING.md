# Things To Do Places To Go - Testing Information

[Website deployed on Heroku](https://things-to-do-project.herokuapp.com/)

[Back to main README.md file](/README.md)

## Testing
- [JSHint - Code Analysis Tool](https://jshint.com/) - used to help detect errors and potential problems in JavaScript code.
- [W3C - Markup Validation Service](https://validator.w3.org/) - used to check the markup validity of the HTML documents.  However some errors were shown due to the presence of the Jinja template language.
- [W3C - CSS Validation Service](https://jigsaw.w3.org/css-validator/) - used to check the validity of the Cascading Style Sheets (CSS).
  Had several Parse Errors but these seem to be caused by my use of CSS variables. Found the following link which explained more why I
  got the errors. [Stackoverflow](https://stackoverflow.com/questions/57661659/w3c-css-validation-parse-error-on-variables)
- [Flake8 within GitPod]() - used to check Python code base against coding style (PEP8)
- [Chrome Developer Tools](https://developers.google.com/web/tools/chrome-devtools) - used to help check the responsiveness of the site and also use of Audits to test for performance, accessibility, best practices & SEO

## User story testing (UX section of README.md)
### Customer
1. How do I search for activities using a word or phrase?

    1. The user would go to the Home page.
    2. Enter their search word or phrase into the text input and press the [Search] button.
    3. A message will be displaying showing how many results were found and what 'word/phrase' they used. If no results are found then a message indicating this will be displayed.
    4. The results of the users search will be displayed as activity cards which the user
    can click on to see further details about an activity.

2. How do I find activities by category.

    1. From the navigation bar the user can choose the 'Activities' drop-down menu.
    2. From this menu select one of the categories to find activities that match.
    3. A message will be displaying showing how many results were found and what [Category] they selected. If no results are found then a message indicating this will be displayed.
    4. The results of the users search will be displayed as activity cards which the user
    can click on to see further details about an activity.

3. How can I submit my own idea for an activity to the database.

    1. To submit an activity the user must be logged-in.
    2. Once logged-in, the user would click on the navigation item 'Submit Activity'
    3. When adding an activity you DO NOT have to choose an image straight-away, this can be added later if you do not have an image to hand. A 'picture not available' image will be displayed for the activity.
    4. Complete the 'Add an Activity' form and click [Add Activity].
    5. If there are any validation errors the user should correct these and click [Add Activity]

4. How can I see all the activiites I have submitted.

    1. The user must be logged-in to view a list of all activities they have submitted.
    2. To view a list of all the activities they have submitted a user can select 'Submitted by Me' option from the profile menu.
    3. The list will be displayed as activity cards which the user can click on to see
    further details about the activity.

5. How can I edit an activity I have submitted.

    1. To edit an activity the user must be logged-in.
    2. Also a user must either have originally submitted the activity or be an admin/moderator to be able to edit an activity.
    3. On an activity card, the user should click on the [Edit] button.
    4. The 'Edit Activity' form is displayed and the user can now edit the required fields and then click [Update Activity].
    5. If there are any validation errors the user should correct these and click [Update Activity]

6. How do I find featured activities.

    1. From the navigation bar the user can choose the 'Activities' drop-down menu.
    2. From this menu select 'Featured'.
    3. A message will be displaying showing 'Featured Activities'.
    4. The results of the 'Featured' search will be displayed as activity cards which the user can click on to see further details about an activity.

7. How do I find newly added activities.

    1. From the navigation bar the user can choose the 'Activities' drop-down menu.
    2. From this menu select 'Recently Added'.
    3. A message will be displaying showing 'Recently Added Activities'.
    4. The results of the 'Recently Added' search will be displayed as activity cards which the user can click on to see further details about an activity.  (Note: only the most recent 6 activites created will be shown)

8. How do I keep a list of my favourite activities.

    1. To keep track of your favourite activities a user must be logged-in.
    2. When viewing the full details of an activity the user can use the 'heart-icon'
    in the top-right of the activity view to either add or remove the activity from their
    'Favourite Activities' list.
    3. To view your Favourite Activity list a user can select 'My Favourites' option from
    the profile menu. The list will be displayed as activity cards which the user can click on to see further details about the activity.

## User story testing (UX section of README.md)
1. How do I play the game?

    1. To find out how to play the game the user clicks the [INSERT COIN] button on the welcome screen and the
    'How to Play' instructions are displayed on the game setup screen.

2. I need to set the game options for skill and select a puzzle image.

    1. After clicking the [INSERT COIN] button on the welcome screen the user can set the game options.
        1. Use the difficulty slider to set how difficult the puzzle will be to solve.
        2. Use the arrows <> next to the puzzle image to select the required image.

3. I want to play the game.

    1. To play the game the user clicks the [INSERT COIN] button on the welcome screen
    2. Sets the game options for difficulty and puzzle image.
    3. Clicks the [PLAY GAME] button.

4. I need to be able to see in-game information about how I’m doing.

    1. In-game information is displayed at the top or left of the screen depending on your device.
    2. There you can see the difficulty level, puzzle preview, count-down timer and moves made.

5. How do I complete the puzzle.

    1. To complete the game the user needs to move the tiles until they are all in their original positions.
    2. Tile moves are done by either clicking or swiping a tile that can move into the blank space.

6. If I get stuck I would like to reset the game.

    1. If the user gets stuck in an existing game they can reset the puzzle by clicking the green [RESET] button.
    2. The puzzle image, count-down timer and moves will all reset and then the game will begin again.

7. I want to end my current game and change the game setup.

    1. To end the current game the user can simply click the red [QUIT] button.
    2. Then to change the setup the user would click the [INSERT COIN] button on the welcome screen.

8. I want to use an image on my device as the puzzle image.

    1. To play the game using an image from their device the user would click the [INSERT COIN] button to get to the
    game options screen.
    2. Use the image select arrows <> to select the last image (image 16 of 16).
    3. Click on the image and then select a JPG image from your device to use as the puzzle image.
    4. The image will be resized, horizontally centered and squared for use as the puzzle image.

9. I want to view the hi-scores table.

    1. To view the hi-scores table click the [HI SCORES] button on the welcome screen.
    2. To exit the hi-scores table the user would wait for the timeout or click the [BACK] button.

10. How do I get on the hi-scores table.

    1. To get on the hi-scores table you need to get a score higher than the lowest displayed in the hi-scores table.
    2. A users score is based on time taken to complete, number of moves and difficulty level.

## Testing elements and functionality of the project (manually tested)

### General
- Make sure that all app pages display as they should.
- Ensure that the logo and navigation display correctly on different device screen sizes.
- Check that the alt/title text appears on the logo image.
- Ensure that font sizes are readable on different devices.
- check that footer social links are working.

### Home page
1. Check the search text input works and the [Search] button functions.

### About page
1. Check that the text displays correctly
2. Ensure that the DB stats are correct.

### Activities (menu)
1. Check that the menu displays as it should on all devices.
2. Ensure each menu option (All, Featured, Recently Added, Animals, Attraction, Crafting, Food, Nature, Sport and Leisure) give the user the expected results.

### Submit/Edit an Activity
1. Confirm all the input fields work as expected and the [Add Activity] button functions and displays processing indicator.
2. Check client-side form validation is working as expected.
3. Check server-side form validation is working as expected.
4. Check [x] link in the top-right allows the user to abort the submit/edit.

### Login/Register
1. Check the email and password input fields work and the [Login] button functions.
2. Check the [Register] button takes the user to the 'User Registration'.
3. At 'User Registration' confirm all the input fields work as expected and the [Register] button functions.
4. Check the 'HERE' to login link works.

### Profile (menu)
1. Check that the menu displays as it should on all devices.
2. Ensure each menu option (View Profile, My Favourites, Submitted by Me, Logout) give the user the expected results.

### Displayed Results (from Activities or Profile menu options)
1. Check that the results are displayed in the correct format depending on the screen size.
2. Has the correct flash message been displayed.
3. Ensure that the image and [i More Details] button link to the full activity view.
4. Check that the [Edit] button only displays if the user originally submitted the
activity or the current user is an admin/moderator.

### Activity View
1. Check that the results are displayed in the correct format depending on the screen size.
2. Ensure that the 'Add to Activity Favourites' heasrt-icon works as expected.
3. Check the alt/title text changes on the heart-icon.
4. Ensure activity links work and only appear if the data is present.
5. Check the 'creator' info at the bottom of the view.

## Additional Testing
1. Asked friends and family to use the application on their phone, tablets and desktops where possible and let me know any issues. Got good feedback, with no real issues.
2. I have tested the site on a desktop using the following modern browsers: Chrome, Firefox and Edge. As well as testing on Android phone/tablet and Apple iPhone.
3. The application has not been written to work on Internet Explorer. In the real World if a client wanted an application to work on IE then that is fine, but a lot of
the newer methods of coding Javascript, etc does not work on IE. IE has had it's day and I wanted to code the app using some of these newer methods.

## Errors/Issues Found
(only includes main errors/issues rather than easy to solve coding, typos, alignment, etc which caused only minor errors)

1. **Uploaded images on Heroku**
As far as user images on this project, I did not realise that we could just use a link
rather than getting the users to actaully upload images. So I did go down the route
of image uploads, cropping, resizing, etc.  This all worked well while testing on GitPod, however when I deployed the site to Heroku the images no longer appeared.
Other than the tutor led course material I had never used Heroku before, so was a
little puzzled but after some Googling I realised that while the image is actually uploaded to Heroku it doesn't actually store the image for very long.  I had a decision to make, undo all the effort and coding I had done for the images or spend time to find a solution. After further investigation I discovered AWS S3 Bucket was a place for my app to upload the images to and serve them back to the users.  This took more time than I thought, but I feel it was well worth it in the end.
