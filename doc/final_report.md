# Final Report of Project Track 1
### Project Report: Changes and Evaluation of the Final Project Compared to Stage 1 Proposal

**1. Changes in the Directions of the Project**
   
   Compared to the initial stage 1 proposal, significant enhancements have been made in presenting course GPA data. Innovatively, the project now incorporates Python's matplotlib to construct bar charts displaying the distribution of different grade scales. This graphical representation allows users to perceive the grade distribution for each course more clearly and intuitively. Additionally, a feature enabling reviewers to rate courses on a scale of 1 to 5 has been introduced, enhancing the ability for users to provide effective feedback on courses.

**2. Application’s Achievements and Shortcomings**

   The application has successfully achieved its goal of making GPA data more accessible and understandable through visual representations. The addition of the rating system further enhances user interaction and feedback mechanisms, making the application not only informative but also interactive. However, one limitation is that without real-time data updates or integration of more dynamic data sources, the information may not reflect the most current trends or changes in course evaluations.

**3. Data Schema and Sources**

   The schema or source of data for the application remained unchanged from the original proposal. It continues to utilize the existing UIUC GPA distribution dataset, ensuring consistency and reliability in the data presented.

**4. Changes to ER Diagram and Table Implementations**

   The ER diagram and table implementations have not been altered in the final design. The decision to maintain the original design was driven by its adequacy in handling the required data and functionalities effectively.

**5. Functionalities Added or Removed**

   The functionality to create bar charts for grade distribution was added to provide a more intuitive understanding of course performance. Conversely, the functionality to scrape comments from RateMyProfessor was removed due to concerns about the relevance and currency of the data, which sometimes contained outdated reviews.

**6. Role of Advanced Database Programs**

   The advanced database programs played a crucial role in efficiently managing and querying the dataset, thereby supporting the application's core functionalities such as data visualization and interaction. These programs facilitated the integration of user feedback through the rating system, enhancing the overall utility and responsiveness of the application.

**7. Future Improvements and Teamwork**

   Future work could include integrating more dynamic data sources to keep the course evaluations up-to-date. Additionally, exploring machine learning models to predict course ratings based on historical data could provide valuable insights to users. 

**8. Teamwork Distribution**

    Shanbin Sun: Frontend development
    Zhixiang Liang: Backend development and data collection
    Jason Barnett: Advanced queries design and testing
    Shuyu Xie: Advanced queries design and testing

**9. Changes Compared to the Original Proposal**

In addition to the technical challenges and solutions described, there were no further changes compared to the original proposal that have not already been discussed. The main adjustments involved the introduction of new features such as the interactive grade distribution charts and modifications to the functionalities planned, like removing outdated comment scraping in favor of more reliable user ratings. These changes were driven by the need to enhance user interaction and the relevance of the information provided.

**10. Technical Challenges and Solutions**

One challenge is that creating efficient SQL queries for complex data aggregation and maintaining quick response times was challenging as data volume grew. The solution is that we can use database optimization through indexing frequently queried columns and refining SQL queries enhanced performance. Use of EXPLAIN statements helped in optimizing query execution. Future projects could further benefit from adding a caching layer.

Another challenge is managing security for dynamic, user-driven queries to prevent SQL injection risks was complex. The solution is that we can safeguarded the system using parameterized queries and stored procedures, focusing on rigorous testing to ensure security and efficiency. Emphasizing security from project inception is crucial, especially with user-generated data.