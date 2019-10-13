//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// Generalized Doc2 Vec Jenkins Job
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

waitTime            = 180
credfile            = './credfile'
project_Id          = 'Project_Id'
git_branch          = 'master'
git_repo            = './Query_Clustering'
time_out            = '240'
sourceFileName      = './instance_config.yml'
monitorFileName     = './monitorconfig.json'


project_Id = "PROJECT_ID:" + projectId
deployment_id = "DEPLOYMENT_ID:" + env.DEPLOYMENT_ID
docker_image =  "DOCKER_IMAGE:" + env.DOCKER_IMAGE
docker_simple = "DOCKER_SIMPLE:" + env.DOCKER_IMAGE.replaceAll('[^a-zA-Z0-9]','-')
email = "EMAIL:" + env.EMAIL
query = "QUERY:" + env.QUERY
prop_value= project_Id + "|" + deployment_id + '|' + docker_image + '|' + docker_simple + "|" + email + "|" query

println "Read all the prop"
echo "${prop_values}"

try {
            stage('Generate Doc2Vec Model'){
                retry(2) {
                    build job: 'build_Instance', parameters: [
                        [$class: 'StringParameterValue', name: 'ADD_PROP', value: prop_values]
                        ], quietPeriod: waitTime
                    }
//                }
            }
//        }
//    }

} catch (e) {
    currentBuild.result = "FAILED"

    throw e
}