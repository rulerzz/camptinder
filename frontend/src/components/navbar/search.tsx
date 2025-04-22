'use client';

import React from 'react';
import { Input } from '../ui/input';
import { BiSearch } from 'react-icons/bi';
const Search = () => {
        return (
                <div className="border-[1px] w-full md:max-w-md xl:max-w-xl px-2 rounded-full shadow-sm hover:shadow-md transition cursor-pointer">
                        <div className="flex flex-row items-center justify-between">
                                <Input
                                        placeholder="Search products..."
                                        className="w-full  border-none shadow-none focus:shadow-none focus-visible:ring-0 focus-visible:ring-offset-0"
                                />
                                <div className="p-2 bg-primary rounded-full text-white hover:bg-primary/80 transition">
                                        <BiSearch size={20} />
                                </div>
                        </div>
                </div>
        );
};

export default Search;
