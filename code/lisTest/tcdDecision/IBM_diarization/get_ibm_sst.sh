path='../playback/STIMULI/english/wavFilesTest/'
out_path='./eng_output_jsons/'
name=$1
# echo $1
curl -X POST -u "apikey:Vt_SAR6Mdpk31Wioi0kZrohPceNZE77dW0rIwaBARGwH" --header "Content-Type: audio/wav" --data-binary @$path$name'.wav' --output $out_path$name'.json' "https://gateway-lon.watsonplatform.net/speech-to-text/api/v1/recognize?model=en-US_BroadbandModel&speaker_labels=true"
# curl -X POST -u "apikey:Vt_SAR6Mdpk31Wioi0kZrohPceNZE77dW0rIwaBARGwH" --header "Content-Type: audio/wav" --data-binary $path$name "https://gateway-lon.watsonplatform.net/speech-to-text/api/v1/recognize"