#!groovy

node {
    env.DOCKER_USE_HUB = 1
    def deployable_branches = ["master", "next_release"]

    stage('Checkout') {
        checkout([$class: 'GitSCM', branches: [[name: ${env.BRANCH_NAME}]], extensions: [[$class: 'SubmoduleOption', disableSubmodules: false,  parentCredentials: true, recursiveSubmodules: true, reference: '', trackingSubmodules: false]]])
        //checkout([$class: 'GitSCM', branches: [[name: '**']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: true, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[]]])
    }

    stage('Docker dev build') {
        echo "Branch is: ${env.BRANCH_NAME}"
        echo "Build is: ${env.BUILD_NUMBER}"
        wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'XTerm']) {
            sh './develop.sh docker_warm_cache'
            sh './develop.sh dev_build'
            sh './develop.sh check_migrations'
        }
    }

    stage('Unit tests') {
        wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'XTerm']) {
            sh './develop.sh runtests'
        }
        step([$class: 'JUnitResultArchiver', testResults: '**/data/tests/*.xml'])
    }

    stage('Lettuce tests') {
        wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'XTerm']) {
            sh './develop.sh dev_lettuce'
        }
        step([$class: 'JUnitResultArchiver', testResults: '**/data/selenium/*.xml'])
        step([$class: 'ArtifactArchiver', artifacts: '**/data/selenium/*.png'])
    }

    if (deployable_branches.contains(env.BRANCH_NAME)) {

        stage('Docker prod build') {
            wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'XTerm']) {
                sh './develop.sh prod_build'
            }
        }

        stage('Publish docker image') {
            withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerbot',
                              usernameVariable: 'DOCKER_USERNAME',
                              passwordVariable: 'DOCKER_PASSWORD']]) {
                wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'XTerm']) {
                    sh './develop.sh ci_docker_login'
                    sh './develop.sh publish_docker_image'
                }
            }
        }
    }
}
