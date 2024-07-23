
# 📰 RPA Quick News 

This automation project was developed in Python and can be run on Robocorp. It uses `Selenium` to interact with the browser and perform extraction of the latest news from the LaTimes website. The robot downloads the featured image of each news item and creates an Excel file (xlsx) with the following information:

- Title
- Date
- Description
- Image file name
- Search phrases count in the title and description
- Indication whether the title or description contains monetary values


The project was developed following object-oriented development practices (OOP). This includes creating classes to encapsulate related functionality, promoting code reuse, ease of maintenance and clarity in the code structure.
## Running

This automation can be run locally or in an environment configured on the Robocorp platform.

To run through Robocorp, consider the following steps:

- Create an account at https://cloud.robocorp.com
- Add a Task Package and define the project source (preferably the project repository on GitHub)
- Create a new process in `Unattended` > `Processes` > `Start from scratch`
- Define the process name and required information in the `General` tab
- In the `Steps` tab, select the task
- Name the step and define the **Worker** that will run the automation. You can define your own Windows machine (Learn more at https://robocorp.com/docs/control-room/unattended/worker-setups/windows-desktop)
- Set environment variables (optional)
- Schedule and Notifications tabs are optional
- Create Process

It is important to note that automation obtains the variables `search_phrase` and `topic_search` from Robocorp Work Items, that can be defined before running the process.

Example of the use of these variables:

| Parameter   | Default       | Description                                 |
| :---------- | :--------- | :------------------------------------------ |
| `search_phrase`      | Economic | Standard search phrase|
| `topic_search`      | Business | News topic that will be selected on the search page |

These parameters will assume the default value if they are not defined in the Work Item.

## Technologies used

- **Python** `3.11.7`
- **Selenium**
- **Robocorp**