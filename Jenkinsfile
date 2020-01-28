pipeline{
	agent any

	    stages{
		
        	    stage('--update repo/push image--'){
			        steps{
                        cd flask_test
                        git pull
                        docker-compose build
                        docker-compose push
            		}
        	}
                stage('--Kubernetes update service--'){
			        steps{
                        cd flask_test
                        kubectl apply -f app.yml
            		}
        	}
        }
}
