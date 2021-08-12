#!/bin/bash

echo "Finding version values..."
# from refs/tags/v1.2.3 get 1.2.3
VERSION=$(echo $GITHUB_REF | sed 's#.*/v##')
PYPROJECT_VERSION=$(poetry run python ./scripts/pyproject.py)

echo "Version found in pyproject.toml: $PYPROJECT_VERSION"

# Set if VERSION was set by manually triggered workflow
if [ ${{ github.event.inputs.version }} != "develop" ]; then
    VERSION=${{ github.event.inputs.version }}
fi

echo "Version found from GitHub: $VERSION"

if [ "$VERSION" > "$PYPROJECT_VERSION" ]; then
    echo "$VERSION is valid. Setting it with poetry..."
    poetry version $VERSION
else
    echo "$VERSION is invalid! It must be greater than $PYPROJECT_VERSION"
    exit 1
fi
