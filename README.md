# FiggleSpeak API

This repository contains a flask API for the project FiggleSpeak, aimed to provide real-time feedback on users' pronunciation and articulation.

We then deploy this API on Google Cloud Run, from which, we interface with in the front end.

## Deployment
### Local Deployment
1. Clone the repository.
2. Create a .env file, and within it add a Hugging Face token, see sample.env for an idea of the format.
3. Within the directory of the cloned repository, run `docker build -t <tag_name> .` in order to build the image.
4. Next, we can run the application in a container using the `docker run` command.

```
$ docker run -e PORT=<port_number> -p <port_number>:<port_number> <tag_name>
```
5. The server may now be accessed at `localhost:<port_number>` or `127.0.0.1:<port_number>`.

For additional help, you may refer to the [Docker documentation on containerising an application](https://docs.docker.com/get-started/02_our_app/).

### Deploying to Google Cloud Run
1. Before deploying to Cloud Run, we first have to push the docker image to a supported container registry. Here, we'll use Artifact Registry.
2. We create a Google Cloud project, and enable Artifact Registry.
3. We need to install the Google Cloud CLI, following the instructions [here](https://cloud.google.com/sdk/docs/install).
4. Create a remote repository in Artifact Registry.
5. Following that, run `gcloud auth configure-docker` to authenticate yourself with your gmail account.
6. Next, we run the following commands, (also found in deploy.sh, however this will require a few modifications):

```
docker build -t figglespeak-api . 
docker tag figglespeak-api gcr.io/<project_id>/figglespeak-api
docker push gcr.io/<project_id>/figglespeak-api
```
7. We may check if the image has been successfully pushed, by checking the Artifact Registry console at https://console.cloud.google.com/artifacts
8. We then go over to Cloud Run, and start a new service.
9. Fill up the form accordingly, however ensure that the memory allocated to the instance is >= 4 Gb. 
10. The server may now be accessed at a location specified on the Google Cloud Run server.

For additional help, you may refer to the [Google Cloud Documentation on deploying to Cloud Run](https://cloud.google.com/run/docs/deploying#other-projects) or the [Google Cloud Documentation on pushing and pulling images from Artifact Registry](https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling).

## Usage
GET '/'
RESPONSE "Hello, world!"

POST '/evaluate_user'

REQUEST
```json
{
	"audio": "# audio clip to be evaluated, in any audio file format",
    "sentence": "# sentence for which the audio clip is to be compared against"
}
```


RESPONSE
```
[
    [
        An array containing an array for the letters of each word, indicating if that portion of that word had been pronounced properly.
    ],

    [
        An array containing pronunciation tips for a phoneme in that word, for each word in the sentence
    ]

]
```
## Technologies Used
* [Flask](https://flask.palletsprojects.com/en/3.0.x/)
* [Docker](https://www.docker.com/)

* [Cloud Run](https://cloud.google.com/run?hl=en)
* [Artifact Registry](https://cloud.google.com/artifact-registry)

* [SpeechBrain](https://speechbrain.github.io/)
* [Torchaudio](https://pytorch.org/audio/stable/index.html)
* [minineedle](https://pypi.org/project/minineedle/)
* [g2p](https://g2p.readthedocs.io/en/latest/?badge=latest) - Grapheme to Phoneme

## Team Members
* [Prannaya Gupta (ThePyProgrammer)](https://github.com/ThePyProgrammer)
* [Lim Lynus (lynusl)](https://github.com/lynusl)
* [Dave Tan (Fasnon)](https://github.com/Fasnon)
* [Lee Jia Jie (mkofdwu)](https://github.com/mkofdwu)