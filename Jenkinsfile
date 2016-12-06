#!groovy

node {
    env.DOCKER_USE_HUB = 1
    def deployable_branches = ["master", "next_release"]
    def artifacts = []
    def testResults = []

    stage('Checkout') {
        checkout scm

        // rdrf git submodule clone is over ssh, project checkout above is over https 
        withCredentials([[$class: 'FileBinding', credentialsId: 'ccgbuildbot_gh_ssh', variable: 'SSH_KEY']]) {
            sh('''
                eval `ssh-agent`
                ssh-add $SSH_KEY
                git submodule update --init
            ''')
        }

    }

    stage('Dev build') {
        echo "Branch is: ${env.BRANCH_NAME}"
        echo "Build is: ${env.BUILD_NUMBER}"
        wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'XTerm']) {
            sh('''
                ./develop.sh docker_warm_cache
                ./develop.sh dev_build
                ./develop.sh check_migrations
            ''')
        }
    }

    testResults = ['**/data/tests/*.xml']
    dockerStage('Unit tests', [], testResults) {
        sh('./develop.sh runtests')
    }

    artifacts = ['**/data/selenium/dev/scratch/*.png', '**/data/selenium/dev/log/*.log']
    testResults = ['**/data/selenium/dev/scratch/*.xml']
    dockerStage('Dev RDRF aloe tests', artifacts, testResults) {
        sh('./develop.sh dev_rdrf_aloe')
    }

    dockerStage('Dev aloe tests', artifacts, testResults) {
        sh('./develop.sh dev_aloe')
    }

    if (deployable_branches.contains(env.BRANCH_NAME)) {

        stage('Prod build') {
            wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'XTerm']) {
                sh('./develop.sh prod_build')
            }
        }

        artifacts = ['**/data/selenium/prod/scratch/*.png', '**/data/selenium/prod/log/*.log']
        testResults = ['**/data/selenium/prod/scratch/*.xml']
        dockerStage('Prod aloe tests', artifacts, testResults) {
            sh('./develop.sh prod_aloe')
        }
 
        stage('Publish docker image') {
            withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerbot',
                              usernameVariable: 'DOCKER_USERNAME',
                              passwordVariable: 'DOCKER_PASSWORD']]) {
                wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'XTerm']) {
                    sh('''
                        ./develop.sh ci_docker_login
                        ./develop.sh publish_docker_image
                    ''')
                }
            }
        }
    }
}


/*
 * dockerStage
 *
 * Custom stage that wraps the stage in timestamps and AnsiColorBuildWrapper
 * Prior to exit wrfy is used to kill all running containers and cleanup.
 */
def dockerStage(String label,
                List<String> artifacts=[],
                List<String> testResults=[],
                Closure body) {

    stage(label) {
        try {
            timestamps {
                wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName':    'XTerm']) {
                    body.call()
                }
            }
        } catch (Exception e) {
            currentBuild.result = 'FAILURE'
            throw e
        } finally {
            for (artifact in artifacts) {
                step([$class: 'ArtifactArchiver', artifacts: artifact, fingerprint: false, excludes: null])
            }
            for (testResult in testResults) {
                step([$class: 'JUnitResultArchiver', testResults: testResult])
            }
            sh('''
                /env/bin/wrfy kill-all --force
                /env/bin/wrfy scrub --force
            ''')
        }
    }
}
