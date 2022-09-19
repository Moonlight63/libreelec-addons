SONARRKEY=1234

RADARRKEY=5678

template="$(cat ./qbitrr.config.toml.template)"
template=$(sed 's/\([^\\]\)"/\1\\"/g; s/^"/\\"/g' <<< "$template")
eval "echo \"${template}\"" >> ./config.test