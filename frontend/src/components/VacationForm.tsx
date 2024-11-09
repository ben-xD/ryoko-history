import React, { useState } from 'react';
import { useForm, useFieldArray, type SubmitHandler, Controller } from 'react-hook-form';
import * as exifr from 'exifr';
import VideoPlayer from './VideoPlayer';

type ExifData = {
  [key: string]: unknown;
  latitude?: number | null;
  longitude?: number | null;
};

interface FormValues {
  names: { name: string }[];
  images: { file: File; exifData: ExifData | null }[];
  description: string;
}

const VacationForm: React.FC = () => {
  const { control, handleSubmit, setValue, register } = useForm<FormValues>({
    defaultValues: {
      names: [{ name: '' }],
      images: [],
      description: '',
    },
  });

  const { fields: nameFields, append: addName } = useFieldArray({
    control,
    name: 'names',
  });

  const [imageFiles, setImageFiles] = useState<FormValues['images']>([]);

  console.log("imageFiles ", imageFiles);

  const handleImageUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    const imagesWithExifData = await Promise.all(
      files.map(async (file) => {
        try {
          const exifData = await exifr.parse(file, { gps: true });
          const latitude = exifData?.GPSLatitude || null;
          const longitude = exifData?.GPSLongitude || null;

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

  const onSubmit: SubmitHandler<FormValues> = (data) => {
    console.log('Form Data:', data);
  };

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)} className="max-w-lg mx-auto p-6 bg-white shadow-md rounded-md space-y-6">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Vacation Form</h2>

        <div>
          <label className="block text-gray-700 font-medium mb-1">Names:</label>
          {nameFields.map((field, index) => (
            <div key={field.id} className="flex items-center space-x-2 mb-2">
              <input
                {...register(`names.${index}.name` as const, { required: 'Name is required' })}
                placeholder="Enter a name"
                className="flex-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {index === nameFields.length - 1 && (
                <button
                  type="button"
                  onClick={() => addName({ name: '' })}
                  className="p-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none"
                >
                  +
                </button>
              )}
            </div>
          ))}
        </div>

        <div>
          <label className="block text-gray-700 font-medium mb-1">Image Upload:</label>
          <input
            type="file"
            accept="image/*"
            multiple
            onChange={handleImageUpload}
            className="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-gray-700 font-medium mb-1">Description:</label>
          <textarea
            {...register('description', { required: 'Description is required' })}
            placeholder="Enter a description"
            className="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <button type="submit" className="w-full p-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none">
          Submit
        </button>
      </form>
      {/* works with local files as well as URL: http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4 */}
      <VideoPlayer url="/videos/holiday_vacation_resort_resort_640.mp4" width="640px" height="360px" />
    </>
  );
};

export default VacationForm;
