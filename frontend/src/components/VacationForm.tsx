import { useMutation } from '@tanstack/react-query';
import * as exifr from 'exifr';
import React, { useState } from 'react';
import { useFieldArray, useForm, type SubmitHandler } from 'react-hook-form';
import { env } from '../env';
import { useAtomValue } from 'jotai';
import { transcriptAtom } from './VoiceAgent';
import VideoPlayer from './VideoPlayer';
import type {CreateTravelSummaryMetadata} from '@/clients/httpClient';
import { Languages } from './Languages';

interface ExifData {
  [key: string]: unknown;
  latitude?: number | null;
  longitude?: number | null;
};

interface TranscriptEntry {
  source: "ai" | "user";
  message: string;
}

interface FormValues {
  names: { name: string }[];
  images: { file: File; exifData: ExifData | null }[];
  description: string;
  transcript: TranscriptEntry[];
  languages: {language: Languages}[];
}

const VacationForm: React.FC = () => {
  const transcript = useAtomValue(transcriptAtom);

  console.log("transcript 💎💎💎 ", transcript)
  
  const { control, handleSubmit, setValue, register } = useForm<FormValues>({
    defaultValues: {
      names: [{ name: '' }],
      images: [],
      description: '',
      languages: [{language: Languages.ENGLISH}]
    },
  });

  const { fields: nameFields, append: addName } = useFieldArray({
    control,
    name: 'names',
  });

  const { fields: languageFields, append: addLanguage } = useFieldArray({
    control,
    name: 'languages',
  });

  const [imageFiles, setImageFiles] = useState<FormValues['images']>([]);

  console.log("imageFiles ", imageFiles);

  const handleImageSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    const imagesWithExifData = await Promise.all(
      files.map(async (file) => {
        try {
          const exifData = await exifr.parse(file, { gps: true });
          const latitude = exifData.GPSLatitude !== undefined ? exifData.latitude : null;
          const longitude = exifData.GPSLongitude !== undefined ? exifData.longitude : null;
          
          return {
            file,
            exifData: {
              ...exifData,
              latitude,
              longitude,
            },
          };
        } catch (error) {
          console.error("Error reading EXIF data:", error);
          return { file, exifData: null };
        }
      })
    );

    setImageFiles((prevFiles) => [...prevFiles, ...imagesWithExifData]); // Append new files to the existing state
    setValue('images', [...imageFiles, ...imagesWithExifData]); // Update form state
  };

  const searchMutation = useMutation({
    // { imageFiles, names: data.names, description: data.description }
    mutationFn: async ({description, imageFiles, names, transcript, languages}: { imageFiles: FormValues['images'], names: string[], description: string, transcript: TranscriptEntry[], languages: Languages[]}) => {

      console.log("transcript >>> ", transcript)
      
      const formData = new FormData();
      for (const file of imageFiles) {
        formData.append('images', file.file);
      }
      formData.append('metadata_json_str', JSON.stringify({names, description, transcript_messages: transcript, languages} satisfies CreateTravelSummaryMetadata));

      const apiPath = "/create-travel-summary/";
      const reply = await fetch(env.backendHttpUrl + apiPath, {
        method: 'POST',
        body: formData,
      });
      return await reply.json()
    },
    onSuccess: (data) => {
      console.log('Success', {data});
    }
  });

  const onSubmit: SubmitHandler<FormValues> = (data) => {
    searchMutation.mutate({
      imageFiles,
      names: data.names.map(n => n.name),
      description: data.description,
      transcript,
      languages: data.languages.map(l => l.language)
    });
  };

  return (
    <div style={{ minHeight: "80vh" }} className="flex flex-col items-center">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="mx-auto my-6 max-w-lg space-y-6 rounded-md bg-white p-6 shadow-md"
      >
        <div>
          <label className="mb-1 block font-medium text-gray-700">Names:</label>
          {nameFields.map((field, index) => (
            <div key={field.id} className="mb-2 flex items-center space-x-2">
              <input
                {...register(`names.${index}.name` as const, { required: 'Name is required' })}
                placeholder="Enter a name"
                className="flex-1 rounded-md border p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {index === nameFields.length - 1 && (
                <button
                  type="button"
                  onClick={() => addName({ name: '' })}
                  className="rounded-md bg-blue-500 p-2 text-white hover:bg-blue-600 focus:outline-none"
                >
                  +
                </button>
              )}
            </div>
          ))}
        </div>
  
        <div>
          <label className="mb-1 block font-medium text-gray-700">Image Upload:</label>
          <input
            type="file"
            accept="image/*"
            multiple
            onChange={handleImageSelect}
            className="w-full rounded-md border p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
      <label className="mb-1 block font-medium text-gray-700">Languages to generate:</label>
      {languageFields.map((field, index) => (
        <div key={field.id} className="mb-2 flex items-center space-x-2">
        <select
          {...register(`languages.${index}.language` as const, { required: 'Language is required' })}
          className="flex-1 rounded-md border p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-700"
        >
          {Object.values(Languages).map((language) => (
            <option key={language} value={language}>
              {language}
            </option>
          ))}
        </select>
        {index === languageFields.length - 1 && (
          <button
            type="button"
            onClick={() => addLanguage({ language: Languages.ENGLISH })}
            className="rounded-md bg-blue-500 p-2 text-white hover:bg-blue-600 focus:outline-none"
          >
            +
          </button>
        )}
      </div>
      ))}
    </div>
  
        <div>
          <label className="mb-1 block font-medium text-gray-700">Description:</label>
          <textarea
            {...register('description', { required: 'Description is required' })}
            placeholder="Enter a description"
            className="w-full rounded-md border p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
  
        <button type="submit" className="w-full rounded-md bg-blue-500 p-2 text-white hover:bg-blue-600 focus:outline-none">
          Submit
        </button>
      </form>
      {/* works with local files as well as URL: http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4 */}
      <VideoPlayer url="/videos/luma-generated.mp4" width="640px" height="360px" />
    </div>
  );  
};

export default VacationForm;
