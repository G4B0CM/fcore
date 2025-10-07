import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'primefaces.org',
        pathname: '/cdn/primereact/**',
      },
    ],
  },
};

export default nextConfig;
