# Bloc n°5 : [Industrialisation d'un algorithme d'apprentissage automatique et automatisation des processus de décision 📁🔍] Mandatory for JedhaBootcamp certification


EMail : fezzibasma@gmail.com                                                                                                                               

# Get-Around 

![image](https://user-images.githubusercontent.com/23299967/208895245-1e88e0d1-3197-4313-8f00-53c177a45bd8.png)

GetAround is the Airbnb for cars. You can rent cars from any person for a few hours to a few days! Founded in 2009, this company has known rapid growth. In 2019, they count over 5 million users and about 20K available cars worldwide.

The purpose of this project is to : 

1 - Build Dashboard analysis with Streamlit and Heroku ! : [Web Dashboard Analysis](https://get-around-dashboard.herokuapp.com)
 
2 - Pricing predictor using 'XGBR' & building API docs with FastAPI and Heroku ! : [Pricing Prediction & FastAPI ](https://getaround-pricing.herokuapp.com/docs#/)
 
 
 To run this project :

## Clone the repository :

git clone https://github.com/fezzibasma/Get-Around.git

## Web Dashboard Analysis ( Follow my steps 🤠 )
 
  Within the directory : web-streamlit

  Data : Get-Around/web-streamlit/prep/get_around_delay_analysis.csv

  ### Deployment :

        Build docker image and run locally :

         - docker run -it -v "$(pwd):/home/app" -p 4000:80 -e PORT=80 jedha/streamlit-sample-app
         
        Get your Heroku app ! :

          - heroku create get-around-dashboard
          - heroku container:push web -a get-around-dashboard
          - heroku container:release web -a get-around-dashboard
          - heroku open -a get-around-dashboard
          
          
          
## Pricing Prediction & FastAPI ( Follow my steps 😎 )
 
  Within the directory : pricing-fastapi

  Data : Get-Around/pricing-fastapi/api/data/get_around_pricing_project.csv

  ### Deployment :

        Build docker image and run locally :

         - docker build . -t apicoco
         - docker run -it -v "$(pwd):/home/app" -p 4000:4000 -e PORT=4000 apicoco
     
    Get your Heroku app ! :

         - heroku create getaround-pricing
         - heroku container:push web -a getaround-pricing
         - heroku container:release web -a getaround-pricing
         - heroku open -a getaround-pricing


 
 

