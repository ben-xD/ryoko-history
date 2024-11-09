import React, { useState } from 'react';
import { useForm, useFieldArray, type SubmitHandler, Controller } from 'react-hook-form';
import * as exifr from 'exifr';

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
    const file = event.target.files![0];
    if (file) {
      try {
        const exifData = await exifr.parse(file, { gps: true });
        if (exifData) {
          // Extract latitude and longitude and add them to exifData
          const latitude = exifData.GPSLatitude ? exifData.latitude : null;
          const longitude = exifData.GPSLongitude ? exifData.longitude : null;

          const exifDataWithLatLong = {
            ...exifData,
            latitude,
            longitude,
          };

          setImageFiles([{ file, exifData: exifDataWithLatLong }]); // Store full exifData with latitude and longitude
          setValue('images', [{ file, exifData: exifDataWithLatLong }]); // Update form with image and full metadata
        }
      } catch (error) {
        console.error("Error reading EXIF data:", error);
      }
    }
  };

  const onSubmit: SubmitHandler<FormValues> = (data) => {
    // Send the data from here to the LLMs
    console.log('Form Data:', data);
  };

  return (
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
  );
};

export default VacationForm;
