pipeline{
	agent any

	stages{
		
		
        	stage('--docker-compose build and push--'){
			steps{
                    		
				cd flask_test/
				git pull
                           	docker-compose build 
                           	docker-compose push
            		}
        	}
		stage('--Replicate services--'){
			steps{
				cd flask_test/
				kubectl apply -f app.yml
			}
		}
	}
}

