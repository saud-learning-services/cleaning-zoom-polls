*This project is still under development. If you are faculty or staff at UBC Sauder School of Business and would like help with this script or have any questions, please put in a ticket at help(at)sauder.ubc.ca, and include mention of the "cleaning-zoom-polls script" in your message.*

# Cleaning Zoom Polls

> See [A detailed explanation with examples](Example.md).

The format of Zoom poll data can be confusing/hard to work with. Each "poll" exists as it's own row of data for a student. If a poll has multiple questions, the row will contain question/answer question/answer order. If a zoom session has multiple polls, a student will have multiple rows of data.

## What Does This Script Do?

This script will read zoom poll files in the `poll_input` folder, and reformat any files to a more readable question/answer format, where for each student and each poll in the file, you will have rows of single questions/answers. These new files can be found in `poll_output`.

### Important Requirements for Zoom Polls
**The script will not work if these are not followed. We have done our best to deal with common errors, and provide some insight into what is missing, but we cannot guarantee we have caught all possible problems.**
- The script expects the files to either be comma-seperated or tab-delimited files
- The script expects to find the columns: "#, "User Name", "User Email", "Submitted Date/Time" in the first row, with data from polls following
- The script expects the file to be the type when downloaded from Zoom, i.e. do not change the file type, or open and resave the original zoom poll file. 
- See Zoom's instructions for [setting up polls](https://support.zoom.us/hc/en-us/articles/213756303-Polling-for-meetings)

#### Some Notes from Zoom:
As of September 3, 2020, https://support.zoom.us/hc/en-us/articles/216378603

 
> <p><strong>Note</strong>:&nbsp;</p>
> <ul>
> <li>Meeting reports are automatically deleted 30 days after the scheduled date. This is also when the meeting is removed the from the&nbsp;<a href="https://zoom.us/meeting?type=previous" target="_blank" rel="noopener"><strong>Previous Meetings</strong></a> page in the web portal.</li>
> <li>If you delete a meeting from your <a href="https://zoom.us/meeting" target="_blank" rel="noopener"><strong>Meetings</strong></a> list in the web portal, you cannot generate reports for that meeting. You can still download any reports you generated before deleting the meeting.</li>
> <li>You should generate meeting reports after your meeting has ended. If generated a report before starting the meeting, you should re-generate the report to obtain the data collected during the meeting.</li>
</ul>

## Steps
- Download your poll files from Zoom, following [Zoom's Instructions](https://support.zoom.us/hc/en-us/articles/216378603)
- Add your poll file(s) to the folder `poll_input`
- Run the script [(see detailed instructions below)](https://github.com/saud-learning-services/cleaning-zoom-polls#running-the-script): **all files in the folder** will be reformatted
- The updated file will be available in `poll_output` with the original name plus "_cleaned"
- If something goes wrong for a file you should see an Error message

## Running the Script

### First Time
We use conda as our main environment manager. If this is your first time, you might need to install the environment. To install environment using conda (only on first run), in terminal run
`conda env create -f environment.yml`

### Every Time
After your environment is created, in terminal:
1. Activate the environment
`conda activate zoom-polls`

1. Navigate to where you have saved the folder `cleaning-zoom-polls`
`cd "YOUR/PATH/cleaning-zoom-polls"`

1. Run the script and follow prompts
`python "parse_zoom_polls.py"`
