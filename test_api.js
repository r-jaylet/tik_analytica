"use strict";

const fetch = require("node-fetch");


const LibraryTrackEnqueueMutation = async libraryTrackId => {
  const mutationDocument = /* GraphQL */ `
    mutation LibraryTrackEnqueueMutation($input: LibraryTrackEnqueueInput!) {
      libraryTrackEnqueue(input: $input) {
        __typename
        ... on LibraryTrackEnqueueSuccess {
          enqueuedLibraryTrack {
            id
            audioAnalysisV6 {
              __typename
            }
          }
        }
        ... on LibraryTrackEnqueueError {
          code
          message
        }
      }
    }
  `;
  const result = await fetch("https://api.cyanite.ai/graphql", {
    method: "POST",
    body: JSON.stringify({
      query: mutationDocument,
      variables: { input: { libraryTrackId } }
    }),
    headers: {
      Authorization: "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiSW50ZWdyYXRpb25BY2Nlc3NUb2tlbiIsInZlcnNpb24iOiIxLjAiLCJpbnRlZ3JhdGlvbklkIjo0NzYsInVzZXJJZCI6MjQwNzksImFjY2Vzc1Rva2VuU2VjcmV0IjoiNzY0YzZkYzA0ZDRjYjk2OWUzMjIwZDRlZWY0MzAyYWM5NmJlM2M0YjY5Njk1NDdhMWNiYmMxNzRiZmQxZmU5NCIsImlhdCI6MTY3ODQ3NTgxMX0.UXnM4_VOas6wZeuST-s3cqdKeF2tl_DSFk9b8f5bdjs",
      "Content-Type": "application/json"
    }
  }).then(res => res.json());
  console.log("[info] LibraryTrackEnqueueMutation response: ");
  console.log(JSON.stringify(result, undefined, 2));
  if (result.data.LibraryTrackEnqueueMutation.__typename.endsWith("Error")) {
    throw new Error(result.data.inDepthAnalysisFileUpload.message);
  }

  return result.data;
};

const main = async libraryTrackId => {
  await LibraryTrackEnqueueMutation('13799870');
};

main(process.argv[2]).catch(err => {
  console.error(err);
  process.exitCode = 1;
});